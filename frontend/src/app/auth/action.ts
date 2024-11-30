'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

import { createClient } from '@/lib/supabase/server'

export async function emailLogin(formData: FormData) {
  const supabase = await createClient()

  // type-casting here for convenience
  // in practice, you should validate your inputs
  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  const { error } = await supabase.auth.signInWithPassword(data)

  if (error) {
    redirect('/auth/login?message=Could not authenticate')
  }

  revalidatePath('/', 'layout')
  redirect('/dashboard')
}

export async function signup(formData: FormData) {
  const supabase = await createClient()

  const email = formData.get('email') as string
  const password = formData.get('password') as string
  const confirmPassword = formData.get('confirmPassword') as string
  const username = formData.get('username') as string

  if (!username?.trim()) {
    redirect('/auth/register?message=Username is required')
  }

  if (password !== confirmPassword) {
    redirect('/auth/register?message=Passwords do not match')
  }

  if (password.length < 6) {
    redirect('/auth/register?message=Password must be at least 6 characters long')
  }

  const { error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      emailRedirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/auth/callback`,
      data: {
        name: username,
        display_name: username,
      }
    },
  })

  if (error) {
    // Handle specific error for duplicate email from Supabase
    if (error.message.toLowerCase().includes('email already registered')) {
      redirect('/auth/register?message=Email already registered. Please use a different email or sign in.')
    }
    redirect('/auth/register?message=' + error.message)
  }

  // Redirect to email confirmation page
  redirect(`/auth/confirm-email?email=${encodeURIComponent(email)}`)
}

export async function signOut() {
  const supabase = await createClient()
  await supabase.auth.signOut()
  revalidatePath('/', 'layout')
  redirect('/')
}