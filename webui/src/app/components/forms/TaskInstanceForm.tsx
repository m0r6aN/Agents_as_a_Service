'use client'

import React, { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"

type TaskInstanceData = {
  id?: string
  taskId: string
  agentId: string
  processId: string
  input: string
  output: string
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  toolIds: string[]
}

type TaskInstanceFormProps = {
  taskInstance: TaskInstanceData | null
  tasks: { id: string; name: string }[]
  agents: { id: string; name: string }[]
  processes: { id: string; name: string }[]
  tools: { id: string; name: string }[]
  onSave: (data: TaskInstanceData) => void
  onClose: () => void
}

export default function TaskInstanceForm({ taskInstance, tasks, agents, processes, tools, onSave, onClose }: TaskInstanceFormProps) {
  const [formData, setFormData] = useState<TaskInstanceData>(taskInstance || {
    taskId: '',
    agentId: '',
    processId: '',
    input: '',
    output: '',
    status: 'pending',
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
    if (taskInstance) {
      setFormData(taskInstance)
    }
  }, [taskInstance])

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{taskInstance ? 'Edit Task Instance' : 'Add New Task Instance'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="taskId">Task</Label>
            <Select name="taskId" value={formData.taskId} onValueChange={handleSelectChange('taskId')}>
              <SelectTrigger>
                <SelectValue placeholder="Select a task" />
              </SelectTrigger>
              <SelectContent>
                {tasks.map((task) => (
                  <SelectItem key={task.id} value={task.id}>{task.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="agentId">Agent</Label>
            <Select name="agentId" value={formData.agentId} onValueChange={handleSelectChange('agentId')}>
              <SelectTrigger>
                <SelectValue placeholder="Select an agent" />
              </SelectTrigger>
              <SelectContent>
                {agents.map((agent) => (
                  <SelectItem key={agent.id} value={agent.id}>{agent.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="processId">Process</Label>
            <Select name="processId" value={formData.processId} onValueChange={handleSelectChange('processId')}>
              <SelectTrigger>
                <SelectValue placeholder="Select a process" />
              </SelectTrigger>
              <SelectContent>
                {processes.map((process) => (
                  <SelectItem key={process.id} value={process.id}>{process.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="input">Input</Label>
            <Textarea
              id="input"
              name="input"
              value={formData.input}
              onChange={handleChange}
              placeholder="Enter task input"
            />
          </div>
          <div>
            <Label htmlFor="output">Output</Label>
            <Textarea
              id="output"
              name="output"
              value={formData.output}
              onChange={handleChange}
              placeholder="Enter task output"
            />
          </div>
          <div>
            <Label htmlFor="status">Status</Label>
            <Select name="status" value={formData.status} onValueChange={handleSelectChange('status')}>
              <SelectTrigger>
                <SelectValue placeholder="Select status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="pending">Pending</SelectItem>
                <SelectItem value="in_progress">In Progress</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
                <SelectItem value="failed">Failed</SelectItem>
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
          <Button type="submit">Save Task Instance</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}