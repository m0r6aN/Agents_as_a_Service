# File: multi_agent_framework/main.py

import asyncio
from process.file_processing_process import FileProcessingProcess
from orchestrator import OrchestratorAgent

async def main():
    # Create and set up the process
    file_process = FileProcessingProcess()
    
    # Create the orchestrator with all agents from the process
    orchestrator = OrchestratorAgent(file_process.agents)
    
    # Set the orchestrator for the process
    file_process.set_orchestrator(orchestrator)

    # Execute the process
    input_data = {"file_path": "/path/to/file.csv"}
    result = await file_process.execute(input_data)
    
    print(f"Process execution completed. Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())