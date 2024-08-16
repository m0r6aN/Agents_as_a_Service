# File: multi_agent_framework/orchestrator.py

from typing import List, Dict, Any
from agents import BaseAgent

class OrchestratorAgent:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = {agent.__class__.__name__: agent for agent in agents}

    async def execute(self, workflow: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        current_task = workflow["start"]

        while current_task:
            task_info = workflow["tasks"][current_task]
            agent = self.agents[task_info["task"]["agent"]]
            action = task_info["task"]["action"]
            
            result = await agent.run_action(action, input_data)
            results[current_task] = result
            input_data.update(result)

            current_task = task_info["next"]

        return results
