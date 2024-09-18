import AIAssistant from "../components/ai-assistant/chat-window";
import ProcessWizard from "../components/process-wizard";

export default function ProcessesPage() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div className="md:col-span-2">
        <h1 className="text-3xl font-bold mb-6">Create New Process</h1>
        <ProcessWizard />
      </div>
      <div>
        <h2 className="text-2xl font-semibold mb-4">AI Assistant</h2>
        <AIAssistant />
      </div>
    </div>
  )
}