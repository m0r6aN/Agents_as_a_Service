'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { supabase } from '@/lib/supabase'

type Tool = {
  id: string
  name: string
  description: string
}

export default function ToolManager() {
  const [tools, setTools] = useState<Tool[]>([])
  const [newTool, setNewTool] = useState({ name: '', description: '' })
  const [editingTool, setEditingTool] = useState<Tool | null>(null)

  useEffect(() => {
    fetchTools()
  }, [])

  async function fetchTools() {
    const { data, error } = await supabase.from('tools').select('*')
    if (error) {
      console.error('Error fetching tools:', error)
    } else {
      setTools(data || [])
    }
  }

  async function addTool() {
    const { data, error } = await supabase
      .from('tools')
      .insert([newTool])
      .select()
    if (error) {
      console.error('Error adding tool:', error)
    } else {
      setTools([...tools, data[0]])
      setNewTool({ name: '', description: '' })
    }
  }

  async function updateTool() {
    if (!editingTool) return
    const { data, error } = await supabase
      .from('tools')
      .update({ name: editingTool.name, description: editingTool.description })
      .eq('id', editingTool.id)
      .select()
    if (error) {
      console.error('Error updating tool:', error)
    } else {
      setTools(tools.map(tool => tool.id === editingTool.id ? data[0] : tool))
      setEditingTool(null)
    }
  }

  async function deleteTool(id: string) {
    const { error } = await supabase
      .from('tools')
      .delete()
      .eq('id', id)
    if (error) {
      console.error('Error deleting tool:', error)
    } else {
      setTools(tools.filter(tool => tool.id !== id))
    }
  }

  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle>{editingTool ? 'Edit Tool' : 'Add New Tool'}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={(e) => {
            e.preventDefault()
            editingTool ? updateTool() : addTool()
          }} className="space-y-4">
            <Input
              placeholder="Tool Name"
              value={editingTool ? editingTool.name : newTool.name}
              onChange={(e) => editingTool 
                ? setEditingTool({...editingTool, name: e.target.value})
                : setNewTool({...newTool, name: e.target.value})
              }
              required
            />
            <Textarea
              placeholder="Tool Description"
              value={editingTool ? editingTool.description : newTool.description}
              onChange={(e) => editingTool
                ? setEditingTool({...editingTool, description: e.target.value})
                : setNewTool({...newTool, description: e.target.value})
              }
              required
            />
            <Button type="submit">{editingTool ? 'Update Tool' : 'Add Tool'}</Button>
            {editingTool && (
              <Button type="button" variant="outline" onClick={() => setEditingTool(null)}>Cancel Edit</Button>
            )}
          </form>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tools.map((tool) => (
          <Card key={tool.id}>
            <CardHeader>
              <CardTitle>{tool.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">{tool.description}</p>
              <div className="flex space-x-2">
                <Button variant="outline" onClick={() => setEditingTool(tool)}>Edit</Button>
                <Button variant="destructive" onClick={() => deleteTool(tool.id)}>Delete</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}