import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface Message {
  id: number
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

export interface Conversation {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
  updatedAt: Date
}

interface ChatStore {
  conversations: Conversation[]
  currentConversationId: string | null
  isLoading: boolean
  error: string | null
  // Actions
  setCurrentConversation: (id: string) => void
  addMessage: (conversationId: string, message: Message) => void
  createConversation: () => void
  deleteConversation: (id: string) => void
  clearConversations: () => void
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      conversations: [],
      currentConversationId: null,
      isLoading: false,
      error: null,

      setCurrentConversation: (id) => {
        set({ currentConversationId: id })
      },

      addMessage: (conversationId, message) => {
        set((state) => ({
          conversations: state.conversations.map((conv) =>
            conv.id === conversationId
              ? {
                  ...conv,
                  messages: [...conv.messages, message],
                  updatedAt: new Date(),
                }
              : conv
          ),
        }))
      },

      createConversation: () => {
        const newConversation: Conversation = {
          id: Date.now().toString(),
          title: 'New Chat',
          messages: [],
          createdAt: new Date(),
          updatedAt: new Date(),
        }
        set((state) => ({
          conversations: [newConversation, ...state.conversations],
          currentConversationId: newConversation.id,
        }))
      },

      deleteConversation: (id) => {
        set((state) => ({
          conversations: state.conversations.filter((conv) => conv.id !== id),
          currentConversationId:
            state.currentConversationId === id ? null : state.currentConversationId,
        }))
      },

      clearConversations: () => {
        set({ conversations: [], currentConversationId: null })
      },
    }),
    {
      name: 'chat-store',
    }
  )
)
