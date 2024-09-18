import Link from 'next/link'
import SearchBar from '../ui/search-bar'
import UserProfile from '../ui/user-profile'

const navItems = [
  { name: 'Processes', href: '/processes' },
  { name: 'Models', href: '/models' },
  { name: 'Tools', href: '/tools' },
  { name: 'Functions', href: '/functions' },
  { name: 'Configs', href: '/configs' },
  { name: 'Secrets', href: '/secrets' },
]

export default function Header() {
  return (
    <header className="bg-white shadow">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="text-2xl font-bold">
          Synthet-IQ
        </Link>
        <nav>
          <ul className="flex space-x-4">
            {navItems.map((item) => (
              <li key={item.name}>
                <Link href={item.href} className="hover:text-blue-600">
                  {item.name}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        <div className="flex items-center space-x-4">
          <SearchBar />
          <UserProfile />
        </div>
      </div>
    </header>
  )
}