import { ModelData } from "../types"


export async function fetchModelTypes(): Promise<string[]> {

  const response = await fetch('/api/model-types')
  return response.json()
}

export async function fetchModelTasks(modelType: string): Promise<string[]> {
  const response = await fetch(`/api/model-tasks?type=${encodeURIComponent(modelType)}`)
  return response.json()
}

export async function saveModel(model: ModelData): Promise<ModelData> {
  const response = await fetch('/api/models', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(model),
  })
  return response.json()
}

export async function updateModel(model: ModelData): Promise<ModelData> {
  const response = await fetch(`/api/models/${model.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(model),
  })
  return response.json()
}