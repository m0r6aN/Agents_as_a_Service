'use client'

import React, { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"

type ModelData = {
  id?: string
  name: string
  description: string
  type: string
  tasks: string[]
  systemMessage: string
  userMessage: string
  temperature: number
  modelSourceUrl: string
  contextWindowSize: number
  usageExample: string
  apiKey: string
  version: string
  author: string
  license: string
  fineTuningStatus: 'Not fine-tuned' | 'Fine-tuned' | 'In progress'
  fineTuningDataset: string
  supportedLanguages: string[]
  inputFormat: string[]
  outputFormat: string[]
  maxSequenceLength: number
  batchSize: number
  quantization: 'None' | 'INT8' | 'FP16'
  hardwareRequirements: string[]
  inferenceTime: number
  modelSize: number
  lastUpdated: string
}

type ModelFormProps = {
  model: ModelData | null
  onSave: (data: ModelData) => void
  onClose: () => void
}

const modelTypes = [
  'Multimodal',
  'Computer Vision',
  'Natural Language Processing',
  'Audio',
  'Tabular',
  'Reinforcement Learning',
  'Other'
]

const tasksByType = {
  'Multimodal': ['Image-Text-to-Text', 'Document Question Answering'],
  'Computer Vision': ['Image Classification', 'Object Detection', 'Image Segmentation'],
  'Natural Language Processing': ['Text Classification', 'Named Entity Recognition', 'Machine Translation'],
  'Audio': ['Speech Recognition', 'Speaker Identification', 'Music Generation'],
  'Tabular': ['Regression', 'Classification', 'Anomaly Detection'],
  'Reinforcement Learning': ['Game Playing', 'Robotics Control', 'Resource Management'],
  'Other': ['Custom Task']
}

export default function ModelForm({ model, onSave, onClose }: ModelFormProps) {
  const [formData, setFormData] = useState<ModelData>(model || {
    name: '',
    description: '',
    type: '',
    tasks: [],
    systemMessage: '',
    userMessage: '',
    temperature: 0.7,
    modelSourceUrl: '',
    contextWindowSize: 2048,
    usageExample: '',
    apiKey: '',
    version: '',
    author: '',
    license: '',
    fineTuningStatus: 'Not fine-tuned',
    fineTuningDataset: '',
    supportedLanguages: [],
    inputFormat: [],
    outputFormat: [],
    maxSequenceLength: 512,
    batchSize: 1,
    quantization: 'None',
    hardwareRequirements: [],
    inferenceTime: 0,
    modelSize: 0,
    lastUpdated: new Date().toISOString().split('T')[0]
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSelectChange = (name: string) => (value: string) => {
    setFormData({ ...formData, [name]: value })
  }

  const handleMultiSelectChange = (name: string) => (value: string[]) => {
    setFormData({ ...formData, [name]: value })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave(formData)
  }

  useEffect(() => {
    if (model) {
      setFormData(model)
    }
  }, [model])

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{model ? 'Edit Model' : 'Add New Model'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter model name"
            />
          </div>
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter model description"
            />
          </div>
          <div>
            <Label htmlFor="type">Type</Label>
            <Select name="type" value={formData.type} onValueChange={handleSelectChange('type')}>
              <SelectTrigger>
                <SelectValue placeholder="Select model type" />
              </SelectTrigger>
              <SelectContent>
                {modelTypes.map((type) => (
                  <SelectItem key={type} value={type}>{type}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="tasks">Tasks</Label>
            <Select 
              name="tasks" 
              value={formData.tasks[0]} 
              onValueChange={(value) => handleMultiSelectChange('tasks')([value])}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select tasks" />
              </SelectTrigger>
              <SelectContent>
                {formData.type && tasksByType[formData.type as keyof typeof tasksByType].map((task) => (
                  <SelectItem key={task} value={task}>{task}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="systemMessage">System Message</Label>
            <Textarea
              id="systemMessage"
              name="systemMessage"
              value={formData.systemMessage}
              onChange={handleChange}
              placeholder="Enter system message"
            />
          </div>
          <div>
            <Label htmlFor="userMessage">User Message (Optional)</Label>
            <Textarea
              id="userMessage"
              name="userMessage"
              value={formData.userMessage}
              onChange={handleChange}
              placeholder="Enter default user message"
            />
          </div>
          <div>
            <Label htmlFor="temperature">Temperature</Label>
            <Input
              id="temperature"
              name="temperature"
              type="number"
              min="0"
              max="1"
              step="0.1"
              value={formData.temperature}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="modelSourceUrl">Model Source URL</Label>
            <Input
              id="modelSourceUrl"
              name="modelSourceUrl"
              value={formData.modelSourceUrl}
              onChange={handleChange}
              placeholder="Enter model source URL"
            />
          </div>
          <div>
            <Label htmlFor="contextWindowSize">Context Window Size</Label>
            <Input
              id="contextWindowSize"
              name="contextWindowSize"
              type="number"
              value={formData.contextWindowSize}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="usageExample">Usage Example</Label>
            <Textarea
              id="usageExample"
              name="usageExample"
              value={formData.usageExample}
              onChange={handleChange}
              placeholder="Enter usage example"
            />
          </div>
          <div>
            <Label htmlFor="apiKey">API Key</Label>
            <Input
              id="apiKey"
              name="apiKey"
              type="password"
              value={formData.apiKey}
              onChange={handleChange}
              placeholder="Enter API key"
            />
          </div>
          <div>
            <Label htmlFor="version">Version</Label>
            <Input
              id="version"
              name="version"
              value={formData.version}
              onChange={handleChange}
              placeholder="Enter model version"
            />
          </div>
          <div>
            <Label htmlFor="author">Author/Organization</Label>
            <Input
              id="author"
              name="author"
              value={formData.author}
              onChange={handleChange}
              placeholder="Enter author or organization"
            />
          </div>
          <div>
            <Label htmlFor="license">License</Label>
            <Input
              id="license"
              name="license"
              value={formData.license}
              onChange={handleChange}
              placeholder="Enter license information"
            />
          </div>
          <div>
            <Label htmlFor="fineTuningStatus">Fine-tuning Status</Label>
            <Select 
              name="fineTuningStatus" 
              value={formData.fineTuningStatus} 
              onValueChange={handleSelectChange('fineTuningStatus')}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select fine-tuning status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Not fine-tuned">Not fine-tuned</SelectItem>
                <SelectItem value="Fine-tuned">Fine-tuned</SelectItem>
                <SelectItem value="In progress">In progress</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="fineTuningDataset">Fine-tuning Dataset</Label>
            <Input
              id="fineTuningDataset"
              name="fineTuningDataset"
              value={formData.fineTuningDataset}
              onChange={handleChange}
              placeholder="Enter fine-tuning dataset"
            />
          </div>
          <div>
            <Label htmlFor="supportedLanguages">Supported Languages</Label>
            <Input
              id="supportedLanguages"
              name="supportedLanguages"
              value={formData.supportedLanguages.join(', ')}
              onChange={(e) => handleMultiSelectChange('supportedLanguages')(e.target.value.split(', '))}
              placeholder="Enter supported languages (comma-separated)"
            />
          </div>
          <div>
            <Label htmlFor="inputFormat">Input Format</Label>
            <Input
              id="inputFormat"
              name="inputFormat"
              value={formData.inputFormat.join(', ')}
              onChange={(e) => handleMultiSelectChange('inputFormat')(e.target.value.split(', '))}
              placeholder="Enter input formats (comma-separated)"
            />
          </div>
          <div>
            <Label htmlFor="outputFormat">Output Format</Label>
            <Input
              id="outputFormat"
              name="outputFormat"
              value={formData.outputFormat.join(', ')}
              onChange={(e) => handleMultiSelectChange('outputFormat')(e.target.value.split(', '))}
              placeholder="Enter output formats (comma-separated)"
            />
          </div>
          <div>
            <Label htmlFor="maxSequenceLength">Maximum Sequence Length</Label>
            <Input
              id="maxSequenceLength"
              name="maxSequenceLength"
              type="number"
              value={formData.maxSequenceLength}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="batchSize">Batch Size</Label>
            <Input
              id="batchSize"
              name="batchSize"
              type="number"
              value={formData.batchSize}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="quantization">Quantization</Label>
            <Select 
              name="quantization" 
              value={formData.quantization} 
              onValueChange={handleSelectChange('quantization')}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select quantization" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="None">None</SelectItem>
                <SelectItem value="INT8">INT8</SelectItem>
                <SelectItem value="FP16">FP16</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="hardwareRequirements">Hardware Requirements</Label>
            <Input
              id="hardwareRequirements"
              name="hardwareRequirements"
              value={formData.hardwareRequirements.join(', ')}
              onChange={(e) => handleMultiSelectChange('hardwareRequirements')(e.target.value.split(', '))}
              placeholder="Enter hardware requirements (comma-separated)"
            />
          </div>
          <div>
            <Label htmlFor="inferenceTime">Inference Time (ms)</Label>
            <Input
              id="inferenceTime"
              name="inferenceTime"
              type="number"
              value={formData.inferenceTime}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="modelSize">Model Size (MB)</Label>
            <Input
              id="modelSize"
              name="modelSize"
              type="number"
              value={formData.modelSize}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="lastUpdated">Last Updated</Label>
            <Input
              id="lastUpdated"
              name="lastUpdated"
              type="date"
              value={formData.lastUpdated}
              onChange={handleChange}
            />
          </div>
          <Button type="submit">Save Model</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}