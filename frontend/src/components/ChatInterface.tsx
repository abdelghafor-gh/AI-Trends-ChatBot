'use client'

import React, { useState, useEffect } from 'react'
import { Send, Loader2, Plus, Trash, Menu } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useChatStore, Message } from '@/lib/store'
import { api } from '@/lib/api'
import { format } from 'date-fns'

export default function ChatInterface() {
  const {
    conversations,
    currentConversationId,
    createConversation,
    addMessage,
    deleteConversation,
    setCurrentConversation,
  } = useChatStore()

  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  // Get current conversation
  const currentConversation = conversations.find(
    (conv) => conv.id === currentConversationId
  )

  // Create a new conversation if none exists
  useEffect(() => {
    if (conversations.length === 0) {
      createConversation()
    }
  }, [conversations.length, createConversation])

  // Close sidebar on mobile when window width is less than 768px
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setIsSidebarOpen(false)
      } else {
        setIsSidebarOpen(true)
      }
    }

    // Initial check
    handleResize()

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputText.trim() || isLoading) return

    setIsLoading(true)

    try {
      // Create a new conversation if none exists
      if (!currentConversationId) {
        const result = await api.chat.createConversation()
        if (result.error) throw new Error(result.error)
        if (result.data) {
          setCurrentConversation(result.data.id)
        }
      }

      // Add user message to the conversation
      const userMessage: Message = {
        id: Date.now().toString(),
        content: inputText,
        role: 'user',
        timestamp: new Date(),
      }
      
      addMessage(currentConversationId!, userMessage)
      setInputText('')

      // Send message to API and get response
      const response = await api.chat.sendMessage(inputText)
      
      if (response.error) {
        throw new Error(response.error)
      }

      // Add AI response to the conversation
      if (response.data) {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: response.data.response,
          role: 'assistant',
          timestamp: new Date(),
        }
        addMessage(currentConversationId!, aiMessage)
      }
    } catch (error) {
      console.error('Error:', error)
      // Optionally add error message to conversation
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: error instanceof Error ? error.message : 'An error occurred',
        role: 'assistant',
        timestamp: new Date(),
      }
      addMessage(currentConversationId!, errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex h-full overflow-hidden">
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        className="md:hidden fixed top-16 left-4 z-50 p-2 bg-white dark:bg-gray-800 rounded-md shadow-lg"
      >
        <Menu className="w-5 h-5" />
      </button>

      {/* Sidebar */}
      <div
        className={cn(
          "fixed md:relative w-64 bg-gray-50 border-r dark:bg-gray-900 dark:border-gray-800 flex flex-col h-full transition-transform duration-300 ease-in-out z-40",
          isSidebarOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        )}
      >
        <div className="p-4 border-b dark:border-gray-800">
          <button
            onClick={() => {
              createConversation()
              if (window.innerWidth < 768) setIsSidebarOpen(false)
            }}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            New Chat
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              className={cn(
                'p-4 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800',
                currentConversationId === conv.id &&
                  'bg-gray-100 dark:bg-gray-800'
              )}
              onClick={() => {
                setCurrentConversation(conv.id)
                if (window.innerWidth < 768) setIsSidebarOpen(false)
              }}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium truncate">
                  {conv.title || 'New Chat'}
                </span>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    deleteConversation(conv.id)
                  }}
                  className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
                >
                  <Trash className="w-4 h-4" />
                </button>
              </div>
              <span className="text-xs text-gray-500">
                {format(new Date(conv.updatedAt), 'MMM d, yyyy')}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Overlay for mobile */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/20 z-30 md:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Chat Area */}
      <div className="flex-1 flex flex-col bg-white dark:bg-gray-950 overflow-hidden relative">
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto p-4 space-y-4">
            {currentConversation?.messages.map((message) => (
              <div
                key={message.id}
                className={cn('flex', {
                  'justify-end': message.role === 'user',
                  'justify-start': message.role === 'assistant',
                })}
              >
                <div
                  className={cn('max-w-[70%] rounded-lg p-3', {
                    'bg-primary text-white': message.role === 'user',
                    'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100':
                      message.role === 'assistant',
                  })}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <span className="text-xs mt-1 opacity-70 block">
                    {format(new Date(message.timestamp), 'HH:mm')}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="border-t dark:border-gray-800 bg-white dark:bg-gray-950">
          <div className="max-w-3xl mx-auto p-4">
            <form
              onSubmit={handleSubmit}
              className="flex items-center space-x-2"
            >
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type your message..."
                disabled={isLoading}
                className="flex-1 px-4 py-3 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:border-gray-700"
              />
              <button
                type="submit"
                disabled={isLoading || !inputText.trim()}
                className={cn(
                  "p-3 rounded-lg transition-colors",
                  "bg-primary text-white hover:bg-primary/90",
                  "disabled:opacity-50 disabled:cursor-not-allowed",
                  "focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
                )}
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
