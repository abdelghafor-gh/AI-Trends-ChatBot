import { create } from 'zustand'
import { api } from './api'
import type { NewsItem, Insight, WeeklySummary } from './api'

interface NewsStore {
  news: NewsItem[]
  trending: NewsItem[]
  insights: Insight[]
  weeklySummary: WeeklySummary | null
  isLoading: boolean
  error: string | null
  
  // Actions
  fetchNews: (category?: string) => Promise<void>
  fetchTrending: () => Promise<void>
  fetchInsights: (category?: string) => Promise<void>
  fetchWeeklySummary: (week?: number, year?: number) => Promise<void>
}

export const useNewsStore = create<NewsStore>((set) => ({
  news: [],
  trending: [],
  insights: [],
  weeklySummary: null,
  isLoading: false,
  error: null,

  fetchNews: async (category) => {
    set({ isLoading: true, error: null })
    const response = await api.news.getNews(category)
    if (response.error) {
      set({ error: response.error })
    } else {
      set({ news: response.data || [] })
    }
    set({ isLoading: false })
  },

  fetchTrending: async () => {
    set({ isLoading: true, error: null })
    const response = await api.news.getTrending()
    if (response.error) {
      set({ error: response.error })
    } else {
      set({ trending: response.data || [] })
    }
    set({ isLoading: false })
  },

  fetchInsights: async (category) => {
    set({ isLoading: true, error: null })
    const response = await api.insights.getInsights(category)
    if (response.error) {
      set({ error: response.error })
    } else {
      set({ insights: response.data || [] })
    }
    set({ isLoading: false })
  },

  fetchWeeklySummary: async (week, year) => {
    set({ isLoading: true, error: null })
    const response = await api.weeklySummary.getSummary(week, year)
    if (response.error) {
      set({ error: response.error })
    } else {
      set({ weeklySummary: response.data || null })
    }
    set({ isLoading: false })
  },
}))