import { UUID } from "crypto"

export interface Task {
  id: string
  name: string
  created_at: string
}

export interface Tool {
  id: string
  name: string
  description: string
  created_at: string
}

export interface Agent {
  id: string
  name: string
  description: string
  created_at: string
}

export interface WorkflowStep {
  id: string
  taskId: string
  agentId: string
  toolIds: string[]
}

export interface ProcessData {
  id: string
  name: string
  description: string
  tasks: Task[]
  tools: Tool[]
  agents: Agent[]
  workflow: WorkflowStep[]
  created_at: string
  updated_at: string
}

export interface Secret {
  id: string
  name: string
  description: string
  updatedAt: string
}

export interface Model{
  id: string
  name: string
  description: string
  size: number
  inference_url: string
  created_at: string
}