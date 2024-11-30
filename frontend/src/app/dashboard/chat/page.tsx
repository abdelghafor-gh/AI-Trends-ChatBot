'use client'

import ChatInterface from '@/components/ChatInterface'

export default function ChatPage() {
  return (
    <div className="h-[calc(100vh-12rem)]">
      <div className="flex h-full flex-col">
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">AI Chat Assistant</h2>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Chat with our AI assistant about the latest trends in artificial intelligence
          </p>
        </div>

        <div className="flex-1">
          <ChatInterface />
        </div>
      </div>
    </div>
  )
}
