
// src/app/components/process-wizard/workflow-step.tsx

import { ProcessData, type WorkflowStep as WorkflowStepType } from 'app/types'
import { useState } from 'react'
import Button from 'app/components/ui/button'

interface WorkflowStepProps {
  processData: ProcessData
  setProcessData: React.Dispatch<React.SetStateAction<ProcessData>>
}

export default function WorkflowStepComponent({ processData, setProcessData }: WorkflowStepProps) {
  const [currentStep, setCurrentStep] = useState<WorkflowStepType>({
    id: '',
    taskId: '',
    agentId: '',
    toolIds: [],
  })

  const addWorkflowStep = () => {
    if (currentStep.taskId && currentStep.agentId) {
      setProcessData((prev) => ({
        ...prev,
        workflow: [...prev.workflow, { ...currentStep, id: Date.now().toString() }],
      }))
      setCurrentStep({ id: '', taskId: '', agentId: '', toolIds: [] })
    }
  }

  const removeWorkflowStep = (id: string) => {
    setProcessData((prev) => ({
      ...prev,
      workflow: prev.workflow.filter((step) => step.id !== id),
    }))
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Define Workflow</h2>
      <div className="space-y-2">
        <select
          value={currentStep.taskId}
          onChange={(e) => setCurrentStep((prev) => ({ ...prev, taskId: e.target.value }))}
          className="w-full p-2 border rounded"
        >
          <option value="">Select a task</option>
          {processData.tasks.map((task) => (
            <option key={task.id} value={task.id}>
              {task.name}
            </option>
          ))}
        </select>
        <select
          value={currentStep.agentId}
          onChange={(e) => setCurrentStep((prev) => ({ ...prev, agentId: e.target.value }))}
          className="w-full p-2 border rounded"
        >
          <option value="">Select an agent</option>
          {processData.agents.map((agent) => (
            <option key={agent.id} value={agent.id}>
              {agent.name}
            </option>
          ))}
        </select>
        <div>
          <p className="font-medium mb-2">Select tools:</p>
          {processData.tools.map((tool) => (
            <label key={tool.id} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={currentStep.toolIds.includes(tool.id)}
                onChange={(e) => {
                  setCurrentStep((prev) => ({
                    ...prev,
                    toolIds: e.target.checked
                      ? [...prev.toolIds, tool.id]
                      : prev.toolIds.filter((id) => id !== tool.id),
                  }))
                }}
              />
              <span>{tool.name}</span>
            </label>
          ))}
        </div>
        <Button onClick={addWorkflowStep}>Add Workflow Step</Button>
      </div>
      <ul className="space-y-2">
        {processData.workflow.map((step) => (
          <li key={step.id} className="flex items-center justify-between p-2 bg-gray-100 rounded">
            <div>
              <span className="font-medium">
                {processData.tasks.find((t) => t.id === step.taskId)?.name}
              </span>
              <span className="mx-2">→</span>
              <span>{processData.agents.find((a) => a.id === step.agentId)?.name}</span>
              <p className="text-sm text-gray-600">
                Tools:{' '}
                {step.toolIds
                  .map((id) => processData.tools.find((t) => t.id === id)?.name)
                  .join(', ')}
              </p>
            </div>
            <Button onClick={() => removeWorkflowStep(step.id)} variant="secondary">
              Remove
            </Button>
          </li>
        ))}
      </ul>
    </div>
  )
}