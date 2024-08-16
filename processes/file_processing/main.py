# File: processes/file_processing/main.py

import asyncio
from core.orchestrator import OrchestratorAgent
from .process import FileProcessingProcess
from .config import PROCESS_CONFIG

async def main():
    process = FileProcessingProcess(PROCESS_CONFIG)
    orchestrator = OrchestratorAgent(process.agents)
    result = await orchestrator.execute(process.workflow, {})
    print(f"Process completed. Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
