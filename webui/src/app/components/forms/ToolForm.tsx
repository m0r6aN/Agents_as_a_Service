'use client'

import React, { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

type ToolData = {
  id?: string
  name: string
  description: string
  configuration: string
}

type ToolFormProps = {
  tool: ToolData | null
  onSave: (data: ToolData) => void
  onClose: () => void
}

export default function ToolForm({ tool, onSave, onClose }: ToolFormProps) {
  const [formData, setFormData] = useState<ToolData>(tool || {
    name: '',
    description: '',
    configuration: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave(formData)
  }

  useEffect(() => {
    if (tool) {
      setFormData(tool)
    }
  }, [tool])

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{tool ? 'Edit Tool' : 'Add New Tool'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter tool name"
            />
          </div>
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter tool description"
            />
          </div>
          <div>
            <Label htmlFor="configuration">Configuration (JSON)</Label>
            <Textarea
              id="configuration"
              name="configuration"
              value={formData.configuration}
              onChange={handleChange}
              placeholder="Enter tool configuration as JSON"
            />
          </div>
          <Button type="submit">Save Tool</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}