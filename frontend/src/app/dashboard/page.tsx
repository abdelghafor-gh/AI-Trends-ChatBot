'use client'

import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import ChatInterface from '@/components/ChatInterface'
import { Card } from '@/components/ui/card'
import { Bell, MessageSquare, TrendingUp } from 'lucide-react'

interface NewsItem {
  title: string
  description: string
  date: string
  source: string
  imageUrl?: string
}

interface Insight {
  title: string
  value: string
  trend: 'up' | 'down'
  change: string
}

const mockNews: NewsItem[] = [
  {
    title: 'OpenAI Announces GPT-5',
    description: 'Latest advancement in language models with unprecedented capabilities in reasoning and multimodal understanding. The new model shows significant improvements in accuracy and reduced hallucinations.',
    date: '2024-03-15',
    source: 'AI News Daily',
    imageUrl: '/news/gpt5.jpg'
  },
  {
    title: 'Google Releases New AI Tools',
    description: 'Revolutionary AI tools for developers and enterprises that promise to transform how businesses interact with artificial intelligence. The suite includes advanced code generation and data analysis tools.',
    date: '2024-03-14',
    source: 'Tech Insider',
    imageUrl: '/news/google-ai.jpg'
  },
  {
    title: 'AI in Healthcare Breakthrough',
    description: 'New AI model achieves 99% accuracy in early disease detection, potentially revolutionizing preventive healthcare. The system has been validated across multiple hospitals and patient demographics.',
    date: '2024-03-13',
    source: 'Health Tech Today',
    imageUrl: '/news/ai-health.jpg'
  }
]

const mockInsights: Insight[] = [
  {
    title: 'AI Market Growth',
    value: '$500B',
    trend: 'up',
    change: '+25%'
  },
  {
    title: 'AI Adoption Rate',
    value: '78%',
    trend: 'up',
    change: '+12%'
  },
  {
    title: 'AI Job Demand',
    value: '150K',
    trend: 'up',
    change: '+30%'
  }
]

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState('news')

  return (
    <div className="container mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
        AI Trends Dashboard
      </h1>

      <Tabs defaultValue="news" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3 lg:w-[400px]">
          <TabsTrigger value="news" className="flex items-center gap-2">
            <Bell className="h-4 w-4" />
            Latest News
          </TabsTrigger>
          <TabsTrigger value="chat" className="flex items-center gap-2">
            <MessageSquare className="h-4 w-4" />
            Chat
          </TabsTrigger>
          <TabsTrigger value="insights" className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            Insights
          </TabsTrigger>
        </TabsList>

        <TabsContent value="news" className="space-y-4">
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Latest AI News</h2>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Stay updated with the most recent developments in AI
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {mockNews.map((news, index) => (
                <Card key={index} className="overflow-hidden">
                  {news.imageUrl && (
                    <div className="h-48 overflow-hidden">
                      <img
                        src={news.imageUrl}
                        alt={news.title}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )}
                  <div className="p-6">
                    <h3 className="font-semibold text-lg text-gray-900 dark:text-white">
                      {news.title}
                    </h3>
                    <p className="mt-2 text-gray-600 dark:text-gray-300 line-clamp-3">
                      {news.description}
                    </p>
                    <div className="flex justify-between items-center mt-4 text-sm text-gray-500 dark:text-gray-400">
                      <span>{news.source}</span>
                      <span>{news.date}</span>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="chat">
          <Card className="p-4">
            <ChatInterface />
          </Card>
        </TabsContent>

        <TabsContent value="insights">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {mockInsights.map((insight, index) => (
              <Card key={index} className="p-6">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  {insight.title}
                </h3>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-3xl font-semibold text-gray-900 dark:text-white">
                    {insight.value}
                  </span>
                  <span className={`text-sm ${
                    insight.trend === 'up' 
                      ? 'text-green-600 dark:text-green-400'
                      : 'text-red-600 dark:text-red-400'
                  }`}>
                    {insight.change}
                  </span>
                </div>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
