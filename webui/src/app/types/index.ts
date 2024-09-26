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

export interface  NodeData{
  label: string
  type: 'task' | 'agent' | 'model' | 'tool'
  name: string
  description: string
  [key: string]: any
}

export interface ModelData {
  id?: string;
  name: string;
  description: string;
  type: string;
  systemMessage: string;
  userMessage: string;
  temperature: number;
  modelSourceUrl: string;
  contextWindowSize: number;
  usageExample: string;
  apiKey: string;
  version: string;
  author: string;
  license: string;
  fineTuningStatus: 'Not fine-tuned' | 'Fine-tuned' | 'In progress';
  fineTuningDataset: string;
  supportedLanguages: string[];
  inputFormat: string[];
  outputFormat: string[];
  maxSequenceLength: number;
  batchSize: number;
  quantization: 'None' | 'INT8' | 'FP16';
  hardwareRequirements: string[];
  inferenceTime: number;
  modelSize: number;
  lastUpdated: string;
}