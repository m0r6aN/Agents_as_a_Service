import { Suspense } from 'react'
import { getFunctions } from '@/lib/functions'

async function FunctionList() {
  const functions = await getFunctions()

  return (
    <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {functions.map((func) => (
        <li key={func.id} className="bg-white shadow rounded-lg p-4">
          <h3 className="text-lg font-semibold">{func.name}</h3>
          <p className="text-sm text-gray-600">{func.description}</p>
          <p className="text-xs text-gray-500 mt-2">Language: {func.language}</p>
        </li>
      ))}
    </ul>
  )
}

export default function FunctionsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Functions</h1>
      <Suspense fallback={<div>Loading functions...</div>}>
        <FunctionList />
      </Suspense>
    </div>
  )
}