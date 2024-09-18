'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import WizardSteps from './process-wizard/wizard-steps'
import DefinitionStep from './process-wizard/definition-step'
import TasksStep from './process-wizard/tasks-step'
import ToolsStep from './process-wizard/tools-step'
import AgentsStep from './process-wizard/agents-step'
import WorkflowStep from './process-wizard/workflow-step'
import Button from '../components/ui/button'
import { ProcessData } from '../types'
import { supabaseAdmin } from '../lib/supabase'

const steps = ['Definition', 'Tasks', 'Tools', 'Agents', 'Workflow']

export default function ProcessWizard() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(0)
  const [processData, setProcessData] = useState<ProcessData>(() => ({
    id: '',
    name: '',
    description: '',
    tasks: [],
    tools: [],
    agents: [],
    workflow: [],
    created_at: '',
    updated_at: '',
  }))

  const handleNext = () => {
    setCurrentStep((prev) => Math.min(prev + 1, steps.length - 1))
  }

  const handlePrevious = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 0))
  }

  const handleSave = async () => {
    try {
      let processId = processData.id

      // Save or update process
      if (!processId) {
        const { data, error } = await supabaseAdmin
          .from('processes')
          .insert({ name: processData.name, description: processData.description })
          .select()
          .single()

        if (error) throw error
        processId = data.id
        setProcessData((prev) => ({ ...prev, id: processId }))
      } else {
        const { error } = await supabaseAdmin
          .from('processes')
          .update({ name: processData.name, description: processData.description })
          .eq('id', processId)

        if (error) throw error
      }

      // Save tasks
      const { error: tasksError } = await supabaseAdmin
        .from('tasks')
        .upsert(
          processData.tasks.map((task) => ({
            id: task.id,
            process_id: processId,
            name: task.name,
          }))
        )

      if (tasksError) throw tasksError

      // Save tools
      const { error: toolsError } = await supabaseAdmin
        .from('process_tools')
        .delete()
        .eq('process_id', processId)

      if (toolsError) throw toolsError

      const { error: newToolsError } = await supabaseAdmin
        .from('process_tools')
        .insert(processData.tools.map((tool) => ({ process_id: processId, tool_id: tool.id })))

      if (newToolsError) throw newToolsError

      // Save agents
      const { error: agentsError } = await supabaseAdmin
        .from('process_agents')
        .delete()
        .eq('process_id', processId)

      if (agentsError) throw agentsError

      const { error: newAgentsError } = await supabaseAdmin
        .from('process_agents')
        .insert(processData.agents.map((agent) => ({ process_id: processId, agent_id: agent.id })))

      if (newAgentsError) throw newAgentsError

      // Save workflow
      const { error: workflowDeleteError } = await supabaseAdmin
        .from('workflow_steps')
        .delete()
        .eq('process_id', processId)

      if (workflowDeleteError) throw workflowDeleteError

      for (const step of processData.workflow) {
        const { data: workflowStep, error: workflowError } = await supabaseAdmin
          .from('workflow_steps')
          .insert({
            process_id: processId,
            task_id: step.taskId,
            agent_id: step.agentId,
          })
          .select()
          .single()

        if (workflowError) throw workflowError

        const { error: workflowToolsError } = await supabaseAdmin
          .from('workflow_tools')
          .insert(
            step.toolIds.map((toolId) => ({
              workflow_step_id: workflowStep.id,
              tool_id: toolId,
            }))
          )

        if (workflowToolsError) throw workflowToolsError
      }

      console.log('Process saved successfully')
      router.push('/processes')
    } catch (error) {
      console.error('Error saving process:', error)
    }
  }

  const renderStep = () => {
    switch (currentStep) {
      case 0:
        return <DefinitionStep processData={processData} setProcessData={setProcessData} />
      case 1:
        return <TasksStep processData={processData} setProcessData={setProcessData} />
      case 2:
        return <ToolsStep processData={processData} setProcessData={setProcessData} />
      case 3:
        return <AgentsStep processData={processData} setProcessData={setProcessData} />
      case 4:
        return <WorkflowStep processData={processData} setProcessData={setProcessData} />
      default:
        return null
    }
  }

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <WizardSteps steps={steps} currentStep={currentStep} />
      <div className="mt-8">{renderStep()}</div>
      <div className="mt-8 flex justify-between">
        <Button onClick={handlePrevious} disabled={currentStep === 0}>
          Previous
        </Button>
        <div>
          <Button onClick={handleSave} variant="secondary" className="mr-4">
            Save
          </Button>
          {currentStep < steps.length - 1 ? (
            <Button onClick={handleNext}>Next</Button>
          ) : (
            <Button onClick={handleSave} variant="default">
              Finish
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}