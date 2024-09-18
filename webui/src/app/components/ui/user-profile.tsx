'use client'

import { useState } from 'react'
import { User, LogOut } from 'lucide-react'

export default function UserProfile() {
  const [isOpen, setIsOpen] = useState(false)

  const handleSignOut = () => {
    // TODO: Implement sign out functionality
    console.log('Signing out')
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-full"
      >
        <User className="text-gray-600" size={24} />
        <span className="text-sm font-medium">John Doe</span>
      </button>
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1">
          <button
            onClick={handleSignOut}
            className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            <LogOut className="inline-block mr-2" size={18} />
            Sign Out
          </button>
        </div>
      )}
    </div>
  )
}