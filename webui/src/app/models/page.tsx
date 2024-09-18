import { Suspense } from 'react'
import { getModels } from '@/lib/models'

async function ModelList() {
  const models = await getModels()

  return (
    <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {models.map((model) => (
        <li key={model.id} className="bg-white shadow rounded-lg p-4">
          <h3 className="text-lg font-semibold">{model.name}</h3>
          <p className="text-sm text-gray-600">{model.description}</p>
        </li>
      ))}
    </ul>
  )
}

export default function ModelsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">AI Models</h1>
      <Suspense fallback={<div>Loading models...</div>}>
        <ModelList />
      </Suspense>
    </div>
  )
}