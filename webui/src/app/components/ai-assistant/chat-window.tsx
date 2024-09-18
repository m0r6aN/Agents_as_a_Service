'use client'

import { useState } from 'react'
import { Send } from 'lucide-react'

interface Message {
  id: number
  text: string
  sender: 'user' | 'ai'
}

export default function AIAssistant() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = { id: Date.now(), text: input, sender: 'user' }
    setMessages((prev) => [...prev, userMessage])
    setInput('')

    // TODO: Implement AI response logic
    const aiMessage: Message = { id: Date.now() + 1, text: 'AI response placeholder', sender: 'ai' }
    setMessages((prev) => [...prev, aiMessage])
  }

  return (
    <div className="bg-white shadow-md rounded-lg p-4 h-[calc(100vh-200px)] flex flex-col">
      <div className="flex-grow overflow-y-auto mb-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-2 p-2 rounded-lg ${
              message.sender === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-100'
            }`}
          >
            {message.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSendMessage} className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-grow mr-2 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <Send size={20} />
        </button>
      </form>
    </div>
  )
}