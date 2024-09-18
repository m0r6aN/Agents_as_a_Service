import { useState, useEffect } from 'react'
import { ProcessData } from 'app/types'
import Button from 'app/components/ui/button'

interface ToolsStepProps {
  processData: ProcessData
  setProcessData: React.Dispatch<React.SetStateAction<ProcessData>>
}

interface Tool {
  id: string
  name: string
  description: string
}

export default function ToolsStep({ processData, setProcessData }: ToolsStepProps) {
  const [availableTools, setAvailableTools] = useState<Tool[]>([])

  useEffect(() => {
    // Fetch available tools from your API or database
    const fetchTools = async () => {
      // Replace this with actual API call
      const tools: Tool[] = [
        { id: '1', name: 'Text Analysis', description: 'Analyze text content' },
        { id: '2', name: 'Image Recognition', description: 'Recognize objects in images' },
        { id: '3', name: 'Data Visualization', description: 'Create charts and graphs' },
      ]
      setAvailableTools(tools)
    }
    fetchTools()
  }, [])

  const toggleTool = (tool: Tool) => {
    setProcessData((prev) => {
      const toolIndex = prev.tools.findIndex((t) => t.id === tool.id)
      if (toolIndex === -1) {
        return { ...prev, tools: [...prev.tools, tool] }
      } else {
        return { ...prev, tools: prev.tools.filter((t) => t.id !== tool.id) }
      }
    })
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Select Tools</h2>
      <ul className="space-y-2">
        {availableTools.map((tool) => (
          <li key={tool.id} className="flex items-center justify-between p-2 bg-gray-100 rounded">
            <div>
              <span className="font-medium">{tool.name}</span>
              <p className="text-sm text-gray-600">{tool.description}</p>
            </div>
            <Button
              onClick={() => toggleTool(tool)}
              variant={processData.tools.some((t) => t.id === tool.id) ? 'secondary' : 'default'}
            >
              {processData.tools.some((t) => t.id === tool.id) ? 'Remove' : 'Add'}
            </Button>
          </li>
        ))}
      </ul>
    </div>
  )
}