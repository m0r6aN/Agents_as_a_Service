import { useState, useEffect } from 'react'
import { ProcessData } from 'app/types'
import Button from 'app/components/ui/button'


interface AgentsStepProps {
  processData: ProcessData
  setProcessData: React.Dispatch<React.SetStateAction<ProcessData>>
}

interface Agent {
  id: string
  name: string
  description: string
}

export default function AgentsStep({ processData, setProcessData }: AgentsStepProps) {
  const [availableAgents, setAvailableAgents] = useState<Agent[]>([])

  useEffect(() => {
    // Fetch available agents from your API or database
    const fetchAgents = async () => {
      // Replace this with actual API call
      const agents: Agent[] = [
        { id: '1', name: 'Data Analyst', description: 'Analyzes and interprets complex data' },
        { id: '2', name: 'Content Creator', description: 'Generates various types of content' },
        { id: '3', name: 'Customer Support', description: 'Handles customer inquiries and issues' },
      ]
      setAvailableAgents(agents)
    }
    fetchAgents()
  }, [])

  const toggleAgent = (agent: Agent) => {
    setProcessData((prev) => {
      const agentIndex = prev.agents.findIndex((a) => a.id === agent.id)
      if (agentIndex === -1) {
        return { ...prev, agents: [...prev.agents, agent] }
      } else {
        return { ...prev, agents: prev.agents.filter((a) => a.id !== agent.id) }
      }
    })
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Select Agents</h2>
      <ul className="space-y-2">
        {availableAgents.map((agent) => (
          <li key={agent.id} className="flex items-center justify-between p-2 bg-gray-100 rounded">
            <div>
              <span className="font-medium">{agent.name}</span>
              <p className="text-sm text-gray-600">{agent.description}</p>
            </div>
            <Button
              onClick={() => toggleAgent(agent)}
              variant={processData.agents.some((a) => a.id === agent.id) ? 'secondary' : 'default'}
            >
              {processData.agents.some((a) => a.id === agent.id) ? 'Remove' : 'Add'}
            </Button>
          </li>
        ))}
      </ul>
    </div>
  )
}