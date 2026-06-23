import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Daily Puzzle',
  description: 'Daily word and number puzzles',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="border-b px-6 py-3 flex items-center justify-between">
          <a href="/" className="font-bold text-xl">Daily Puzzle</a>
          <a href="/login" className="text-sm underline">Login</a>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  )
}
