'use client'

import React, { useState, useEffect } from 'react'
import { Send, Loader2, Plus, Trash } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useChatStore } from '@/lib/store'
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

  const handleSendMessage = async (e?: React.FormEvent) => {
    e?.preventDefault()
    
    if (!inputText.trim() || isLoading || !currentConversationId) return

    const userMessage = {
      id: Date.now(),
      text: inputText.trim(),
      sender: 'user' as const,
      timestamp: new Date(),
    }

    // Add user message to conversation
    addMessage(currentConversationId, userMessage)
    setInputText('')
    setIsLoading(true)

    try {
      // Send message to API
      const response = await api.chat.sendMessage(inputText)

      if (response.error) throw new Error(response.error)

      // Add bot response to conversation
      const botMessage = {
        id: Date.now() + 1,
        text: response.data?.response || 'Sorry, I could not process your message.',
        sender: 'bot' as const,
        timestamp: new Date(),
      }

      addMessage(currentConversationId, botMessage)
    } catch (error) {
      console.error('Error sending message:', error)
      // Add error message to conversation
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, there was an error processing your message. Please try again.',
        sender: 'bot' as const,
        timestamp: new Date(),
      }
      addMessage(currentConversationId, errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex h-full overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-gray-50 border-r dark:bg-gray-900 dark:border-gray-800 flex flex-col">
        <div className="p-4 border-b dark:border-gray-800">
          <button
            onClick={() => createConversation()}
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
              onClick={() => setCurrentConversation(conv.id)}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium truncate">
                  {conv.title}
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

      {/* Chat Area */}
      <div className="flex-1 flex flex-col bg-white dark:bg-gray-950 overflow-hidden">
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto p-4 space-y-4">
            {currentConversation?.messages.map((message) => (
              <div
                key={message.id}
                className={cn('flex', {
                  'justify-end': message.sender === 'user',
                  'justify-start': message.sender === 'bot',
                })}
              >
                <div
                  className={cn('max-w-[70%] rounded-lg p-3', {
                    'bg-primary text-white': message.sender === 'user',
                    'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100':
                      message.sender === 'bot',
                  })}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.text}</p>
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
              onSubmit={handleSendMessage}
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
