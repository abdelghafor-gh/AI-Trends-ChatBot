import { Message, Conversation } from './store'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const FASTAPI_BASE_URL = process.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:9000'

export interface ApiResponse<T> {
  data?: T
  error?: string
}

export interface NewsItem {
  title: string
  description: string
  url: string
  source: string
  imageUrl?: string
  publishedAt: Date
  category: string[]
}

export interface Insight {
  title: string
  content: string
  keyPoints: string[]
  sources: string[]
  createdAt: Date
  category: string[]
}

export interface WeeklySummary {
  weekNumber: number
  year: number
  highlights: string[]
  topNews: NewsItem[]
  keyInsights: Insight[]
  trends: string[]
  createdAt: Date
}

class ChatAPI {
  private baseUrl = API_BASE_URL
  private fastapiUrl = FASTAPI_BASE_URL

  async getConversations(): Promise<ApiResponse<Conversation[]>> {
    const response = await fetch(`${this.baseUrl}/conversations`)
    if (!response.ok) {
      throw new Error('Failed to fetch conversations')
    }
    const data = await response.json()
    return { data }
  }

  async createConversation(): Promise<ApiResponse<Conversation>> {
    const response = await fetch(`${this.baseUrl}/conversations`, {
      method: 'POST',
    })
    if (!response.ok) {
      throw new Error('Failed to create conversation')
    }
    const data = await response.json()
    return { data }
  }

  async deleteConversation(id: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/conversations/${id}`, {
      method: 'DELETE',
    })
    if (!response.ok) {
      throw new Error('Failed to delete conversation')
    }
  }

  async clearConversations(): Promise<void> {
    const response = await fetch(`${this.baseUrl}/conversations`, {
      method: 'DELETE',
    })
    if (!response.ok) {
      throw new Error('Failed to clear conversations')
    }
  }

  async addMessage(conversationId: string, message: Message): Promise<void> {
    const response = await fetch(
      `${this.baseUrl}/conversations/${conversationId}/messages`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(message),
      }
    )
    if (!response.ok) {
      throw new Error('Failed to add message')
    }
  }

  async sendMessage(message: string): Promise<ApiResponse<{ response: string }>> {
    try {
      const response = await fetch(`${this.fastapiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to send message');
      }
      
      const data = await response.json()
      return { data }
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Failed to send message' }
    }
  }
}

// export const chatApi = new ChatAPI()

export const api = {
  // Chat endpoints
  chat: new ChatAPI(),

  // News endpoints
  news: {
    getNews: async (category?: string, days: number = 7): Promise<ApiResponse<NewsItem[]>> => {
      try {
        const params = new URLSearchParams()
        if (category) params.append('category', category)
        if (days) params.append('days', days.toString())
        
        const res = await fetch(`${API_BASE_URL}/news?${params}`)
        if (!res.ok) throw new Error('Failed to fetch news')
        return { data: await res.json() }
      } catch (error) {
        return { error: error instanceof Error ? error.message : 'Failed to fetch news' }
      }
    },

    getTrending: async (): Promise<ApiResponse<NewsItem[]>> => {
      try {
        const res = await fetch(`${API_BASE_URL}/news/trending`)
        if (!res.ok) throw new Error('Failed to fetch trending news')
        return { data: await res.json() }
      } catch (error) {
        return { error: error instanceof Error ? error.message : 'Failed to fetch trending news' }
      }
    }
  },

  // Insights endpoints
  insights: {
    getInsights: async (category?: string): Promise<ApiResponse<Insight[]>> => {
      try {
        const params = new URLSearchParams()
        if (category) params.append('category', category)
        
        const res = await fetch(`${API_BASE_URL}/insights?${params}`)
        if (!res.ok) throw new Error('Failed to fetch insights')
        return { data: await res.json() }
      } catch (error) {
        return { error: error instanceof Error ? error.message : 'Failed to fetch insights' }
      }
    }
  },

  // Weekly summary endpoints
  weeklySummary: {
    getSummary: async (week?: number, year?: number): Promise<ApiResponse<WeeklySummary>> => {
      try {
        const params = new URLSearchParams()
        if (week) params.append('week', week.toString())
        if (year) params.append('year', year.toString())
        
        const res = await fetch(`${API_BASE_URL}/weekly-summary?${params}`)
        if (!res.ok) throw new Error('Failed to fetch weekly summary')
        return { data: await res.json() }
      } catch (error) {
        return { error: error instanceof Error ? error.message : 'Failed to fetch weekly summary' }
      }
    }
  }
}