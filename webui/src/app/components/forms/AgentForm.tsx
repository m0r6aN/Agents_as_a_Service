'use client'

import React, { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"

type AgentData = {
  id?: string
  name: string
  description: string
  modelId: string
  toolIds: string[]
}

type AgentFormProps = {
  agent: AgentData | null
  models: { id: string; name: string }[]
  tools: { id: string; name: string }[]
  onSave: (data: AgentData) => void
  onClose: () => void
}

export default function AgentForm({ agent, models, tools, onSave, onClose }: AgentFormProps) {
  const [formData, setFormData] = useState<AgentData>(agent || {
    name: '',
    description: '',
    modelId: '',
    toolIds: [],
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSelectChange = (name: string) => (value: string) => {
    setFormData({ ...formData, [name]: value })
  }

  const handleToolChange = (toolId: string) => {
    setFormData(prev => ({
      ...prev,
      toolIds: prev.toolIds.includes(toolId)
        ? prev.toolIds.filter(id => id !== toolId)
        : [...prev.toolIds, toolId]
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave(formData)
  }

  useEffect(() => {
    if (agent) {
      setFormData(agent)
    }
  }, [agent])

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{agent ? 'Edit Agent' : 'Add New Agent'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter agent name"
            />
          </div>
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter agent description"
            />
          </div>
          <div>
            <Label htmlFor="modelId">Model</Label>
            <Select name="modelId" value={formData.modelId} onValueChange={handleSelectChange('modelId')}>
              <SelectTrigger>
                <SelectValue placeholder="Select a model" />
              </SelectTrigger>
              <SelectContent>
                {models.map((model) => (
                  <SelectItem key={model.id} value={model.id}>{model.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label>Tools</Label>
            <div className="space-y-2">
              {tools.map((tool) => (
                <div key={tool.id} className="flex items-center space-x-2">
                  <Checkbox
                    id={`tool-${tool.id}`}
                    checked={formData.toolIds.includes(tool.id)}
                    onCheckedChange={() => handleToolChange(tool.id)}
                  />
                  <label
                    htmlFor={`tool-${tool.id}`}
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    {tool.name}
                  </label>
                </div>
              ))}
            </div>
          </div>
          <Button type="submit">Save Agent</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}