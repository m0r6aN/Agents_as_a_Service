import { ProcessData } from '../../types'

interface DefinitionStepProps {
  processData: ProcessData
  setProcessData: React.Dispatch<React.SetStateAction<ProcessData>>
}

export default function DefinitionStep({ processData, setProcessData }: DefinitionStepProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setProcessData((prev) => ({ ...prev, [name]: value }))
  }

  return (
    <div className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Process Name
        </label>
        <input
          type="text"
          id="name"
          name="name"
          value={processData.name}
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          rows={4}
          value={processData.description}
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>
    </div>
  )
}