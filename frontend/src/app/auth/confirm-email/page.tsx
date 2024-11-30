import { Card } from '@/components/ui/card'
import { Mail } from 'lucide-react'

export default function ConfirmEmailPage({
  searchParams,
}: {
  searchParams: { email?: string }
}) {
  const email = searchParams.email || 'your email'

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 dark:bg-gray-900">
      <Card className="w-full max-w-md space-y-6 p-8">
        <div className="flex flex-col items-center space-y-4 text-center">
          <div className="rounded-full bg-primary/10 p-4">
            <Mail className="h-8 w-8 text-primary" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Check your email
          </h1>
          <p className="text-gray-500 dark:text-gray-400">
            We sent a verification link to
            <br />
            <span className="font-medium text-gray-900 dark:text-white">
              {email}
            </span>
          </p>
        </div>
        <div className="space-y-4 text-sm text-gray-500 dark:text-gray-400">
          <p>
            Please check your email and click the verification link to complete
            your registration.
          </p>
          <p>
            If you don&apos;t see the email, check your spam folder. The link will
            expire in 24 hours.
          </p>
        </div>
      </Card>
    </div>
  )
}
