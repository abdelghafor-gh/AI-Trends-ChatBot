'use client'

import { useEffect, useState } from 'react'
import { auth } from '@/auth'

export default function InsightsPage() {
  const [insights, setInsights] = useState({
    totalConversations: 0,
    popularTopics: ['AI', 'Machine Learning', 'Data Science'],
    userEngagement: {
      dailyActive: 120,
      weeklyActive: 850,
      monthlyActive: 2400
    }
  })

  useEffect(() => {
    // Fetch insights data from your backend
    const fetchInsights = async () => {
      // Implement API call to get insights
    }
    fetchInsights()
  }, [])

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">AI Trends Insights</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Total Conversations Card */}
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Total Conversations</h2>
            <p className="text-4xl font-bold">{insights.totalConversations}</p>
          </div>
        </div>

        {/* Popular Topics Card */}
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Popular Topics</h2>
            <div className="space-y-2">
              {insights.popularTopics.map((topic, index) => (
                <div key={index} className="badge badge-primary badge-lg">{topic}</div>
              ))}
            </div>
          </div>
        </div>

        {/* User Engagement Card */}
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">User Engagement</h2>
            <div className="stats stats-vertical shadow">
              <div className="stat">
                <div className="stat-title">Daily Active</div>
                <div className="stat-value">{insights.userEngagement.dailyActive}</div>
              </div>
              <div className="stat">
                <div className="stat-title">Weekly Active</div>
                <div className="stat-value">{insights.userEngagement.weeklyActive}</div>
              </div>
              <div className="stat">
                <div className="stat-title">Monthly Active</div>
                <div className="stat-value">{insights.userEngagement.monthlyActive}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}