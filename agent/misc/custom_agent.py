from core.base_agent import BaseAgent
from typing import Dict, Any, List

class CustomAgent(BaseAgent):
    def __init__(self, known_actions: Dict[str, callable], default_prompt: str, system_message: str = "", max_turns: int = 5):
        super().__init__(known_actions, default_prompt, system_message, max_turns)
        self.tools: List[Tool] = []

    def add_tool(self, tool: Tool):
        """
        Add a tool to the agent's toolset.

        :param tool: The tool object to be added.
        """
        self.tools.append(tool)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main function using the input data.
        
        :param input_data: The input data required for execution.
        :return: The output data after execution.
        """
        # Agent-specific execution logic
        task_description = input_data.get('task_description')
        print(f"Executing task: {task_description}")
        return {"result": "success"}

    async def query(self, question: str) -> str:
        """
        Query the agent with a question and return its response.
        
        :param question: The question to ask the agent.
        :return: The agent's response as a string.
        """
        return f"Processing query: {question}"
