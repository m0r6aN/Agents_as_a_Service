import { Suspense } from 'react'
import { getSecrets } from '@/lib/secrets'

async function SecretList() {
  const secrets = await getSecrets()

  return (
    <ul className="space-y-4">
      {secrets.map((secret) => (
        <li key={secret.id} className="bg-white shadow rounded-lg p-4">
          <h3 className="text-lg font-semibold">{secret.name}</h3>
          <p className="text-sm text-gray-600">{secret.description}</p>
          <p className="text-xs text-gray-500 mt-2">Last updated: {secret.updatedAt}</p>
        </li>
      ))}
    </ul>
  )
}

export default function SecretsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Secrets</h1>
      <Suspense fallback={<div>Loading secrets...</div>}>
        <SecretList />
      </Suspense>
    </div>
  )
}