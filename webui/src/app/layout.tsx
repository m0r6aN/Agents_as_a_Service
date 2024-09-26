import { Inter } from 'next/font/google'
import '../styles/globals.css'
import Header from './components/layouts/header'
import Footer from './components/layouts/footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Synthet-IQ',
  description: 'AI-powered cloud-based process management',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} flex flex-col min-h-screen`}>
        <Header />
        <main className="flex-grow container mx-auto px-4 py-8">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}