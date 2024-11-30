import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import Link from 'next/link'

export default async function Home() {
  // Check if user is authenticated
  const supabase = await createClient()
  const { data: { session } } = await supabase.auth.getSession()

  // If authenticated, redirect to dashboard
  if (session) {
    redirect('/dashboard')
  }

  // If not authenticated, show the welcome page
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center space-y-12">
          <div className="space-y-4">
            <h1 className="text-5xl font-bold text-gray-900 dark:text-white">
              AI Trends ChatBot
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Your intelligent companion for exploring the latest trends in artificial intelligence, technology, and innovation.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-md">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Real-time Insights
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Get up-to-date information about the latest AI developments and trends
              </p>
            </div>
            <div className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-md">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Interactive Chat
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Engage in natural conversations to explore specific AI topics and trends
              </p>
            </div>
            <div className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-md">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Personalized Experience
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Receive tailored insights based on your interests and queries
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <Link
              href="/auth/login"
              className="inline-block px-6 py-3 text-lg bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Get Started
            </Link>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Don't have an account?{' '}
              <Link href="/auth/register" className="text-indigo-600 hover:text-indigo-500 dark:text-indigo-400">
                Sign up now
              </Link>
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
