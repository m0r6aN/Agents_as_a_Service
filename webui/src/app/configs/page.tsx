import { Suspense } from 'react'
import { getConfigs } from '../lib/configs'

async function ConfigList() {
  const configs = await getConfigs()

  return (
    <ul className="space-y-4">
      {configs.map((config) => (
        <li key={config.id} className="bg-white shadow rounded-lg p-4">
          <h3 className="text-lg font-semibold">{config.name}</h3>
          <p className="text-sm text-gray-600">{config.description}</p>
          <pre className="mt-2 bg-gray-100 p-2 rounded text-sm overflow-x-auto">
            {JSON.stringify(config.value, null, 2)}
          </pre>
        </li>
      ))}
    </ul>
  )
}

export default function ConfigsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Configurations</h1>
      <Suspense fallback={<div>Loading configurations...</div>}>
        <ConfigList />
      </Suspense>
    </div>
  )
}