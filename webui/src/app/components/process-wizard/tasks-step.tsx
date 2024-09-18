import { useState } from 'react'
import { ProcessData } from 'app/types'
import Button from 'app/components/ui/button'

interface TasksStepProps {
  processData: ProcessData
  setProcessData: React.Dispatch<React.SetStateAction<ProcessData>>
}

export default function TasksStep({ processData, setProcessData }: TasksStepProps) {
  const [newTask, setNewTask] = useState('')

  const addTask = () => {
    if (newTask.trim()) {
      setProcessData((prev) => ({
        ...prev,
        tasks: [...prev.tasks, { id: Date.now().toString(), name: newTask.trim() }],
      }))
      setNewTask('')
    }
  }

  const removeTask = (id: string) => {
    setProcessData((prev) => ({
      ...prev,
      tasks: prev.tasks.filter((task) => task.id !== id),
    }))
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Define Tasks</h2>
      <div className="flex space-x-2">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Enter a new task"
          className="flex-grow p-2 border rounded"
        />
        <Button onClick={addTask}>Add Task</Button>
      </div>
      <ul className="space-y-2">
        {processData.tasks.map((task) => (
          <li key={task.id} className="flex items-center justify-between p-2 bg-gray-100 rounded">
            <span>{task.name}</span>
            <Button onClick={() => removeTask(task.id)} variant="secondary">
              Remove
            </Button>
          </li>
        ))}
      </ul>
    </div>
  )
}