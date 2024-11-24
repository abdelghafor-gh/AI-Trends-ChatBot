import ChatInterface from '@/components/ChatInterface'
import { auth } from '@/auth'

export default async function Home() {
  const session = await auth()

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto space-y-8">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
                AI Trends ChatBot
              </h1>
              <p className="text-lg text-gray-600 dark:text-gray-300">
                Stay updated with the latest AI trends and news through our intelligent chatbot
              </p>
            </div>

            {session ? (
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-600 dark:text-gray-300">
                  Welcome, {session.user?.name}
                </span>
                <form action="/api/auth/signout" method="POST">
                  <button
                    type="submit"
                    className="px-4 py-2 text-sm text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                  >
                    Sign Out
                  </button>
                </form>
              </div>
            ) : (
              <a
                href="/api/auth/signin"
                className="px-4 py-2 text-sm bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
              >
                Sign In
              </a>
            )}
          </div>
          
          {session ? (
            <ChatInterface />
          ) : (
            <div className="text-center py-12">
              <p className="text-lg text-gray-600 dark:text-gray-300">
                Please sign in to start chatting
              </p>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
