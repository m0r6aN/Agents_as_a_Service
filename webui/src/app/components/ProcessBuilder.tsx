'use client'

import React, { useState, useCallback, useEffect } from 'react'
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Connection,
  BackgroundVariant,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { Button } from "@/components/ui/button"
import ModelForm from '@/components/forms/ModelForm'
import AgentForm from '@/components/forms/AgentForm'
import TaskInstanceForm from '@/components/forms/TaskInstanceForm'

import ToolForm from '@/components/forms/ToolForm'
import { saveModel, updateModel, saveAgent, updateAgent, saveTaskInstance, updateTaskInstance, saveTool, updateTool, fetchModels, fetchAgents, fetchTasks, fetchProcesses, fetchTools } from '@/lib/api'
import TaskNode from '@/components/nodes/TaskNode'
import AgentNode from '@/components/nodes/AgentNode'
import ModelNode from '@/components/nodes/ModelNode'
import ToolNode from '@/components/nodes/ToolNode'

const nodeTypes = {
  task: TaskNode,
  agent: AgentNode,
  model: ModelNode,
  tool: ToolNode,
}

export default function ProcessBuilder() {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [showModelForm, setShowModelForm] = useState(false)
  const [showAgentForm, setShowAgentForm] = useState(false)
  const [showTaskInstanceForm, setShowTaskInstanceForm] = useState(false)
  const [showToolForm, setShowToolForm] = useState(false)
  const [selectedModel, setSelectedModel] = useState(null)
  const [selectedAgent, setSelectedAgent] = useState(null)
  const [selectedTaskInstance, setSelectedTaskInstance] = useState(null)
  const [selectedTool, setSelectedTool] = useState(null)
  const [models, setModels] = useState([])
  const [agents, setAgents] = useState([])
  const [tasks, setTasks] = useState([])
  const [processes, setProcesses] = useState([])
  const [tools, setTools] = useState([])

  useEffect(() => {
    fetchModels().then(setModels)
    fetchAgents().then(setAgents)
    fetchTasks().then(setTasks)
    fetchProcesses().then(setProcesses)
    fetchTools().then(setTools)
  }, [])

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  const addNode = (type: 'task' | 'agent' | 'model' | 'tool') => {
    const newNode: Node = {
      id: (nodes.length + 1).toString(),
      type,
      data: { label: `New ${type}`, type },
      position: { x: Math.random() * 500, y: Math.random() * 500 },
    }
    setNodes((nds) => nds.concat(newNode))
  }

  const handleAddModel = () => {
    setSelectedModel(null)
    setShowModelForm(true)
  }

  const handleAddAgent = () => {
    setSelectedAgent(null)
    setShowAgentForm(true)
  }

  const handleAddTaskInstance = () => {
    setSelectedTaskInstance(null)
    setShowTaskInstanceForm(true)
  }

  const handleAddTool = () => {
    setSelectedTool(null)
    setShowToolForm(true)
  }

  const handleSaveModel = async (modelData) => {
    try {
      let savedModel
      if (modelData.id) {
        savedModel = await updateModel(modelData)
      } else {
        savedModel = await saveModel(modelData)
      }
      setModels((prevModels) => [...prevModels.filter(m => m.id !== savedModel.id), savedModel])
      setShowModelForm(false)
    } catch (error) {
      console.error('Error saving model:', error)
    }
  }

  const handleSaveAgent = async (agentData) => {
    try {
      let savedAgent
      if (agentData.id) {
        savedAgent = await updateAgent(agentData)
      } else {
        savedAgent = await saveAgent(agentData)
      }
      setAgents((prevAgents) => [...prevAgents.filter(a => a.id !== savedAgent.id), savedAgent])
      setShowAgentForm(false)
    } catch (error) {
      console.error('Error saving agent:', error)
    }
  }

  const handleSaveTaskInstance = async (taskInstanceData) => {
    try {
      let savedTaskInstance
      if (taskInstanceData.id) {
        savedTaskInstance = await updateTaskInstance(taskInstanceData)
      } else {
        savedTaskInstance = await saveTaskInstance(taskInstanceData)
      }
      const newNode = {
        id: savedTaskInstance.id,
        type: 'task',
        data: savedTaskInstance,
        position: { x: Math.random() * 500, y: Math.random() * 500 },
      }
      setNodes((nds) => nds.concat(newNode))
      setShowTaskInstanceForm(false)
    } catch (error) {
      console.error('Error saving task instance:', error)
    }
  }

  const handleSaveTool = async (toolData) => {
    try {
      let savedTool
      if (toolData.id) {
        savedTool = await updateTool(toolData)
      } else {
        savedTool = await saveTool(toolData)
      }
      setTools((prevTools) => [...prevTools.filter(t => t.id !== savedTool.id), savedTool])
      setShowToolForm(false)
    } catch (error) {
      console.error('Error saving tool:', error)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex space-x-2 mb-4">
        <Button onClick={handleAddTaskInstance}>Add Task Instance</Button>
        <Button onClick={handleAddAgent}>Add Agent</Button>
        <Button onClick={handleAddModel}>Add Model</Button>
        <Button onClick={handleAddTool}>Add Tool</Button>
      </div>
      <div style={{ width: '100%', height: '500px' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
        >
          <Controls />
          <MiniMap />
          <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
        </ReactFlow>
      </div>
      {showModelForm && (
        <ModelForm
          model={selectedModel}
          onSave={handleSaveModel}
          onClose={() => setShowModelForm(false)}
        />
      )}
      {showAgentForm && (
        <AgentForm
          agent={selectedAgent}
          models={models}
          tools={tools}
          onSave={handleSaveAgent}
          onClose={() => setShowAgentForm(false)}
        />
      )}
      {showTaskInstanceForm && (
        <TaskInstanceForm
          taskInstance={selectedTaskInstance}
          tasks={tasks}
          agents={agents}
          processes={processes}
          tools={tools}
          onSave={handleSaveTaskInstance}
          onClose={() => setShowTaskInstanceForm(false)}
        />
      )}
      {showToolForm && (
        <ToolForm
          tool={selectedTool}
          onSave={handleSaveTool}
          onClose={() => setShowToolForm(false)}
        />
      )}
    </div>
  )
}