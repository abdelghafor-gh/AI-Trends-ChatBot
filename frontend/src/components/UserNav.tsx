'use client'

import { useEffect, useState } from 'react'
import { User, LogOut, Settings, CreditCard } from 'lucide-react'
import { createClient } from '@/lib/supabase/client'
import { signOut } from '@/app/auth/action'
import { cn } from '@/lib/utils'

export function UserNav() {
  const [userEmail, setUserEmail] = useState<string | null>(null)
  const [userName, setUserName] = useState<string | null>(null)
  const [initials, setInitials] = useState<string>('U')
  const [avatarUrl, setAvatarUrl] = useState<string | null>(null)

  useEffect(() => {
    const fetchUserData = async () => {
      const supabase = createClient()
      const { data: { user } } = await supabase.auth.getUser()
      
      if (user?.email) {
        setUserEmail(user.email)
        // Get name from user metadata
        const displayName = user.user_metadata?.display_name || user.user_metadata?.name
        const name = displayName || user.email?.split('@')[0] || 'User'
        setUserName(name)
        // Create initials from name
        const initials = name
          .split(' ')
          .map((n: string) => n[0])
          .join('')
          .toUpperCase()
          .slice(0, 2)
        setInitials(initials)
        // Get avatar URL if exists
        setAvatarUrl(user.user_metadata?.avatar_url || null)
      }
    }

    fetchUserData()
  }, [])

  return (
    <div className="flex items-center gap-4">
      <div className="dropdown dropdown-end">
        <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar">
          <div className={cn(
            "w-10 rounded-full flex items-center justify-center text-primary",
            "bg-primary/10"
          )}>
            {avatarUrl ? (
              <img src={avatarUrl} alt={userName || ''} />
            ) : (
              <span className="text-lg font-semibold">{initials}</span>
            )}
          </div>
        </div>
        <ul tabIndex={0} className="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
          <li className="menu-title px-4 py-2">
            <div className="flex flex-col">
              <span className="font-semibold">{userName}</span>
              <span className="text-xs opacity-60">{userEmail}</span>
            </div>
          </li>
          <div className="divider my-0"></div>
          <li>
            <a className="flex items-center gap-3">
              <User className="w-4 h-4" />
              Profile
            </a>
          </li>
          <li>
            <a className="flex items-center gap-3">
              <CreditCard className="w-4 h-4" />
              Billing
            </a>
          </li>
          <li>
            <a className="flex items-center gap-3">
              <Settings className="w-4 h-4" />
              Settings
            </a>
          </li>
          <div className="divider my-0"></div>
          <li>
            <form action={signOut}>
              <button className="flex w-full items-center gap-3 text-error">
                <LogOut className="w-4 h-4" />
                Log out
              </button>
            </form>
          </li>
        </ul>
      </div>
    </div>
  )
}
