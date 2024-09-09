# agents/slm_llm_agent.py

from agents.base_agent import BaseAgent
from tools.language_model_tool import LanguageModelTool

class SLM_LLM_Agent(BaseAgent):
    def __init__(self, slm_tool: LanguageModelTool, llm_tool: LanguageModelTool, config: dict):
        known_actions = {
            'process_data': self.process_data
        }
        default_prompt = "Process the following data."
        super().__init__(known_actions, default_prompt, system_message="SLM/LLM Agent Initialized", max_turns=5)
        self.slm_tool = slm_tool
        self.llm_tool = llm_tool
        self.config = config

    async def _execute_task(self, input_data: dict) -> dict:
        # Decide whether to use SLM or LLM based on task complexity
        prompt = input_data.get('prompt', self.default_prompt)
        if self.is_complex_task(input_data):
            result = self.llm_tool.execute(prompt)
        else:
            result = self.slm_tool.execute(prompt)

        return {"status": "success", "result": result}

    def is_complex_task(self, input_data: dict) -> bool:
        """
        Determine if the task is complex enough to require an LLM.
        """
        # Implement your logic here (e.g., based on task type, data size, etc.)
        return len(input_data.get('prompt', "")) > 100

    async def query(self, question: str) -> str:
        return f"SLM_LLM_Agent received the question: {question}"
