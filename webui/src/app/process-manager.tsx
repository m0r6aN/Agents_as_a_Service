'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd'
import Button from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import {Card, CardHeader, CardTitle, CardContent} from '@/components/ui/card'
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { PlusCircle, Trash2, GripVertical } from 'lucide-react'
import { supabase } from '@/lib/supabase'

type Model = {
  id: string
  name: string
  description: string
  size: number
  inference_url: string
}

type Agent = {
  id: string
  name: string
  description: string
  model_id: string
  inference_url: string
}

type Tool = {
  id: string
  name: string
  description: string
}

type Task = {
  id: string
  name: string
  input: string
  required_agent_capability: string
  expected_output: string
  agent_id: string
  dependencies: string[]
}

type Process = {
  id: string
  name: string
  description: string
  tasks: Task[]
}

export default function ProcessManager() {
  const [process, setProcess] = useState<Process>({
    id: '',
    name: '',
    description: '',
    tasks: []
  })
  const [agents, setAgents] = useState<Agent[]>([])
  const [models, setModels] = useState<Model[]>([])
  const [tools, setTools] = useState<Tool[]>([])
  const router = useRouter()

  useEffect(() => {
    fetchAgentsModelsAndTools()
  }, [])

  const fetchAgentsModelsAndTools = async () => {
    const { data: agentsData, error: agentsError } = await supabase
      .from('agents')
      .select('*, models(*)')
    const { data: toolsData, error: toolsError } = await supabase
      .from('tools')
      .select('*')
    const { data: modelsData, error: modelsError } = await supabase
      .from('models')
      .select('*')

    if (agentsError) console.error('Error fetching agents:', agentsError)
    else setAgents(agentsData || [])

    if (toolsError) console.error('Error fetching tools:', toolsError)
    else setTools(toolsData || [])

    if (modelsError) console.error('Error fetching models:', modelsError)
    else setModels(modelsData || [])
  }

  const handleProcessChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setProcess({ ...process, [e.target.name]: e.target.value })
  }

  const addTask = () => {
    const newTask: Task = {
      id: crypto.randomUUID(),
      name: '',
      input: '',
      required_agent_capability: '',
      expected_output: '',
      agent_id: '',
      dependencies: []
    }
    setProcess({ ...process, tasks: [...process.tasks, newTask] })
  }

  const handleTaskChange = (taskId: string, field: keyof Task, value: any) => {
    setProcess({
      ...process,
      tasks: process.tasks.map(task =>
        task.id === taskId ? { ...task, [field]: value } : task
      )
    })
  }

  const removeTask = (taskId: string) => {
    setProcess({
      ...process,
      tasks: process.tasks.filter(task => task.id !== taskId)
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically send the process data to your backend
    console.log('Submitting process:', process)
    // After successful submission, redirect to the processes list
    router.push('/processes')
  }

  const onDragEnd = (result: any) => {
    if (!result.destination) {
      return
    }

    const newTasks = Array.from(process.tasks)
    const [reorderedTask] = newTasks.splice(result.source.index, 1)
    newTasks.splice(result.destination.index, 0, reorderedTask)

    setProcess({ ...process, tasks: newTasks })
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Process Manager</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Process Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              name="name"
              value={process.name}
              onChange={handleProcessChange}
              placeholder="Process Name"
              required
            />
            <Textarea
              name="description"
              value={process.description}
              onChange={handleProcessChange}
              placeholder="Process Description"
              required
            />
          </CardContent>
        </Card>

        <DragDropContext onDragEnd={onDragEnd}>
          <Droppable droppableId="tasks">
            {(provided) => (
              <div {...provided.droppableProps} ref={provided.innerRef}>
                <Accordion type="single" collapsible className="w-full">
                  {process.tasks.map((task, index) => (
                    <Draggable key={task.id} draggableId={task.id} index={index}>
                      {(provided) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          className="mb-4"
                        >
                          <AccordionItem value={task.id}>
                            <AccordionTrigger className="text-left group">
                              <div className="flex items-center w-full">
                                <div {...provided.dragHandleProps} className="mr-2">
                                  <GripVertical className="h-5 w-5 text-gray-400" />
                                </div>
                                <span>Task {index + 1}: {task.name || 'Unnamed Task'}</span>
                              </div>
                            </AccordionTrigger>
                            <AccordionContent>
                              <Card>
                                <CardContent className="space-y-4 pt-4">
                                  <Input
                                    value={task.name}
                                    onChange={(e) => handleTaskChange(task.id, 'name', e.target.value)}
                                    placeholder="Task Name"
                                    required
                                  />
                                  <Input
                                    value={task.input}
                                    onChange={(e) => handleTaskChange(task.id, 'input', e.target.value)}
                                    placeholder="Input"
                                    required
                                  />
                                  <Input
                                    value={task.required_agent_capability}
                                    onChange={(e) => handleTaskChange(task.id, 'required_agent_capability', e.target.value)}
                                    placeholder="Required Agent Capability"
                                    required
                                  />
                                  <Input
                                    value={task.expected_output}
                                    onChange={(e) => handleTaskChange(task.id, 'expected_output', e.target.value)}
                                    placeholder="Expected Output"
                                    required
                                  />
                                  <Select
                                    value={task.agent_id}
                                    onValueChange={(value) => handleTaskChange(task.id, 'agent_id', value)}
                                  >
                                    <SelectTrigger>
                                      <SelectValue placeholder="Select Agent" />
                                    </SelectTrigger>
                                    <SelectContent>
                                      {agents.map((agent) => (
                                        <SelectItem key={agent.id} value={agent.id}>
                                          {agent.name} - Model: {models.find(m => m.id === agent.model_id)?.name}
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                  <Select>
                                    <SelectTrigger>
                                      <SelectValue placeholder="Select Tools" />
                                    </SelectTrigger>
                                    <SelectContent>
                                      {tools.map((tool) => (
                                        <SelectItem key={tool.id} value={tool.id}>
                                          {tool.name}
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                  <Button type="button" variant="destructive" onClick={() => removeTask(task.id)}>
                                    Remove Task
                                  </Button>
                                </CardContent>
                              </Card>
                            </AccordionContent>
                          </AccordionItem>
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </Accordion>
              </div>
            )}
          </Droppable>
        </DragDropContext>

        <Button type="button" onClick={addTask} className="w-full">
          <PlusCircle className="mr-2 h-4 w-4" /> Add Task
        </Button>

        <Button type="submit" className="w-full">Save Process</Button>
      </form>
    </div>
  )
}