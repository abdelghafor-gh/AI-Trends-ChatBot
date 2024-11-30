import Link from 'next/link'
import { Bell, MessageSquare, TrendingUp } from 'lucide-react'
import { UserNav } from '@/components/UserNav'
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

const navigation = [
  { name: 'Latest News', href: '/dashboard', icon: Bell },
  { name: 'Chat', href: '/dashboard/chat', icon: MessageSquare },
  { name: 'Insights', href: '/dashboard/insights', icon: TrendingUp },
]

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // Check if user is authenticated
  const supabase = await createClient()
  const { data: { session } } = await supabase.auth.getSession()

  if (!session) {
    redirect('/auth/login')
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm dark:bg-gray-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-14 justify-between">
            <div className="flex">
              <div className="flex flex-shrink-0 items-center">
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                  AI Trends Hub
                </h1>
              </div>
              <div className="ml-6 flex space-x-8">
                {navigation.map((item) => {
                  const Icon = item.icon
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-700 dark:text-gray-300 dark:hover:text-gray-200 focus:outline-none border-b-2 border-transparent hover:border-blue-500 dark:hover:border-blue-400"
                    >
                      <Icon className="mr-2 h-4 w-4" />
                      {item.name}
                    </Link>
                  )
                })}
              </div>
            </div>

            <UserNav />
          </div>
        </div>
      </nav>

      <main className="pt-14">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
    </div>
  )
}
