'use client'

import { Card } from '@/components/ui/card'
import { TrendingUp, TrendingDown, Users, Brain, DollarSign, Briefcase } from 'lucide-react'

interface Insight {
  title: string
  value: string
  trend: 'up' | 'down'
  change: string
  description: string
  icon: any
}

const insights: Insight[] = [
  {
    title: 'AI Market Growth',
    value: '$500B',
    trend: 'up',
    change: '+25%',
    description: 'Global AI market size and its year-over-year growth',
    icon: DollarSign
  },
  {
    title: 'AI Adoption Rate',
    value: '78%',
    trend: 'up',
    change: '+12%',
    description: 'Percentage of enterprises implementing AI solutions',
    icon: Brain
  },
  {
    title: 'AI Job Demand',
    value: '150K',
    trend: 'up',
    change: '+30%',
    description: 'Number of AI-related job openings worldwide',
    icon: Briefcase
  },
  {
    title: 'AI Research Papers',
    value: '25K',
    trend: 'up',
    change: '+15%',
    description: 'Monthly published AI research papers',
    icon: Users
  }
]

export default function InsightsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">AI Industry Insights</h2>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Key metrics and trends in the AI industry
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {insights.map((insight, index) => {
          const Icon = insight.icon
          const TrendIcon = insight.trend === 'up' ? TrendingUp : TrendingDown
          
          return (
            <Card key={index} className="p-6">
              <div className="flex items-center justify-between">
                <Icon className="h-8 w-8 text-gray-400" />
                <div className={`flex items-center ${
                  insight.trend === 'up' 
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-red-600 dark:text-red-400'
                }`}>
                  <TrendIcon className="h-4 w-4 mr-1" />
                  <span className="text-sm font-medium">{insight.change}</span>
                </div>
              </div>
              
              <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">
                {insight.title}
              </h3>
              
              <div className="mt-1">
                <span className="text-2xl font-bold text-gray-900 dark:text-white">
                  {insight.value}
                </span>
              </div>
              
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                {insight.description}
              </p>
            </Card>
          )
        })}
      </div>

      <div className="mt-12 grid gap-6 lg:grid-cols-2">
        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Top AI Technologies
          </h3>
          <div className="space-y-4">
            {[
              { name: 'Large Language Models', percentage: 85 },
              { name: 'Computer Vision', percentage: 75 },
              { name: 'Robotics', percentage: 60 },
              { name: 'Speech Recognition', percentage: 70 }
            ].map((tech, index) => (
              <div key={index}>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {tech.name}
                  </span>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {tech.percentage}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${tech.percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Industry Adoption
          </h3>
          <div className="space-y-4">
            {[
              { name: 'Healthcare', percentage: 72 },
              { name: 'Finance', percentage: 88 },
              { name: 'Manufacturing', percentage: 65 },
              { name: 'Retail', percentage: 58 }
            ].map((industry, index) => (
              <div key={index}>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {industry.name}
                  </span>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {industry.percentage}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                  <div
                    className="bg-green-600 h-2 rounded-full"
                    style={{ width: `${industry.percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}
