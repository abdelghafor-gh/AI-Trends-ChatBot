import React from 'react'
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI Trends ChatBot',
  description: 'An AI-powered chatbot for discussing AI trends',
  keywords: ['AI', 'chatbot', 'artificial intelligence', 'news', 'trends'],
  authors: [{ name: 'Abdelghafor', url: 'https://github.com/Abdelghafor-az/AI-Trends-ChatBot' }],
  openGraph: {
    title: 'AI Trends ChatBot',
    description: 'Stay updated with the latest AI trends through our intelligent chatbot',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            <Navbar />
            {children}
          </ThemeProvider>
        </Providers>
      </body>
    </html>
  )
}