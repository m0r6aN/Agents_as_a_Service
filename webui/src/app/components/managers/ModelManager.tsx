'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { supabase } from '@/lib/supabase'

type Model = {
  id: string
  name: string
  description: string
  size: number
  inference_url: string
  temperature: number
  max_tokens: number
  top_p: number
  version: string
  pricing: number
}

export default function ModelManager() {
  const [models, setModels] = useState<Model[]>([])
  const [newModel, setNewModel] = useState({
    name: '',
    description: '',
    size: 0,
    inference_url: '',
    temperature: 0.7,
    max_tokens: 100,
    top_p: 1,
    version: '1.0',
    pricing: 0
  })
  const [editingModel, setEditingModel] = useState<Model | null>(null)

  useEffect(() => {
    fetchModels()
  }, [])

  async function fetchModels() {
    const { data, error } = await supabase.from('models').select('*')
    if (error) {
      console.error('Error fetching models:', error)
    } else {
      setModels(data || [])
    }
  }

  async function addModel() {
    const { data, error } = await supabase
      .from('models')
      .insert([newModel])
      .select()
    if (error) {
      console.error('Error adding model:', error)
    } else {
      setModels([...models, data[0]])
      setNewModel({
        name: '',
        description: '',
        size: 0,
        inference_url: '',
        temperature: 0.7,
        max_tokens: 100,
        top_p: 1,
        version: '1.0',
        pricing: 0
      })
    }
  }

  async function updateModel() {
    if (!editingModel) return
    const { data, error } = await supabase
      .from('models')
      .update(editingModel)
      .eq('id', editingModel.id)
      .select()
    if (error) {
      console.error('Error updating model:', error)
    } else {
      setModels(models.map(model => model.id === editingModel.id ? data[0] : model))
      setEditingModel(null)
    }
  }

  async function deleteModel(id: string) {
    const { error } = await supabase
      .from('models')
      .delete()
      .eq('id', id)
    if (error) {
      console.error('Error deleting model:', error)
    } else {
      setModels(models.filter(model => model.id !== id))
    }
  }

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle>{editingModel ? 'Edit Model' : 'Add New Model'}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={(e) => {
            e.preventDefault()
            editingModel ? updateModel() : addModel()
          }} className="space-y-4">
            <Input
              placeholder="Model Name"
              value={editingModel ? editingModel.name : newModel.name}
              onChange={(e) => editingModel 
                ? setEditingModel({...editingModel, name: e.target.value})
                : setNewModel({...newModel, name: e.target.value})
              }
              required
            />
            <Textarea
              placeholder="Model Description"
              value={editingModel ? editingModel.description : newModel.description}
              onChange={(e) => editingModel
                ? setEditingModel({...editingModel, description: e.target.value})
                : setNewModel({...newModel, description: e.target.value})
              }
              required
            />
            <Input
              type="number"
              placeholder="Model Size"
              value={editingModel ? editingModel.size : newModel.size}
              onChange={(e) => {
                const size = parseInt(e.target.value)
                editingModel
                  ? setEditingModel({...editingModel, size})
                  : setNewModel({...newModel, size})
              }}
              required
            />
            <Input
              placeholder="Inference URL"
              value={editingModel ? editingModel.inference_url : newModel.inference_url}
              onChange={(e) => editingModel
                ? setEditingModel({...editingModel, inference_url: e.target.value})
                : setNewModel({...newModel, inference_url: e.target.value})
              }
              required
            />
            <Input
              type="number"
              step="0.1"
              placeholder="Temperature"
              value={editingModel ? editingModel.temperature : newModel.temperature}
              onChange={(e) => {
                const temperature = parseFloat(e.target.value)
                editingModel
                  ? setEditingModel({...editingModel, temperature})
                  : setNewModel({...newModel, temperature})
              }}
              required
            />
            <Input
              type="number"
              placeholder="Max Tokens"
              value={editingModel ? editingModel.max_tokens : newModel.max_tokens}
              onChange={(e) => {
                const max_tokens = parseInt(e.target.value)
                editingModel
                  ? setEditingModel({...editingModel, max_tokens})
                  : setNewModel({...newModel, max_tokens})
              }}
              required
            />
            <Input
              type="number"
              step="0.1"
              placeholder="Top P"
              value={editingModel ? editingModel.top_p : newModel.top_p}
              onChange={(e) => {
                const top_p = parseFloat(e.target.value)
                editingModel
                  ? setEditingModel({...editingModel, top_p})
                  : setNewModel({...newModel, top_p})
              }}
              required
            />
            <Input
              placeholder="Version"
              value={editingModel ? editingModel.version : newModel.version}
              onChange={(e) => editingModel
                ? setEditingModel({...editingModel, version: e.target.value})
                : setNewModel({...newModel, version: e.target.value})
              }
              required
            />
            <Input
              type="number"
              step="0.001"
              placeholder="Pricing (per 1000 tokens)"
              value={editingModel ? editingModel.pricing : newModel.pricing}
              onChange={(e) => {
                const pricing = parseFloat(e.target.value)
                editingModel
                  ? setEditingModel({...editingModel, pricing})
                  : setNewModel({...newModel, pricing})
              }}
              required
            />
            <Button type="submit">{editingModel ? 'Update Model' : 'Add Model'}</Button>
            {editingModel && (
              <Button type="button" variant="outline" onClick={() => setEditingModel(null)}>Cancel Edit</Button>
            )}
          </form>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {models.map((model) => (
          <Card key={model.id}>
            <CardHeader>
              <CardTitle>{model.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-2">{model.description}</p>
              <p className="text-sm text-gray-600 mb-2">Size: {model.size}</p>
              <p className="text-sm text-gray-600 mb-2">URL: {model.inference_url}</p>
              <p className="text-sm text-gray-600 mb-2">Temperature: {model.temperature}</p>
              <p className="text-sm text-gray-600 mb-2">Max Tokens: {model.max_tokens}</p>
              <p className="text-sm text-gray-600 mb-2">Top P: {model.top_p}</p>
              <p className="text-sm text-gray-600 mb-2">Version: {model.version}</p>
              <p className="text-sm text-gray-600 mb-4">Pricing: ${model.pricing.toFixed(3)} per 1000 tokens</p>
              <div className="flex space-x-2">
                <Button variant="outline" onClick={() => setEditingModel(model)}>Edit</Button>
                <Button variant="destructive" onClick={() => deleteModel(model.id)}>Delete</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}