import { Suspense } from 'react'
import { getTools } from '@/lib/tools'

async function ToolList() {
  const tools = await getTools()

  return (
    <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {tools.map((tool) => (
        <li key={tool.id} className="bg-white shadow rounded-lg p-4">
          <h3 className="text-lg font-semibold">{tool.name}</h3>
          <p className="text-sm text-gray-600">{tool.description}</p>
        </li>
      ))}
    </ul>
  )
}

export default function ToolsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Tools</h1>
      <Suspense fallback={<div>Loading tools...</div>}>
        <ToolList />
      </Suspense>
    </div>
  )
}