from openai import OpenAI
from typing import Callable, Dict, Any
from ...core.base_agent import BaseAgent

class GPT4Agent(BaseAgent):
    def __init__(self, known_actions: Dict[str, Callable], default_prompt: str, api_key: str, system_message: str = "", max_turns: int = 5):
        super().__init__(known_actions, default_prompt, system_message, max_turns)
       
        openai.api_key = api_key

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Use the agent's logic or GPT-4 to process input data and return the result
        self.add_message("user", input_data.get("message", ""))
        response = await self.query(self.default_prompt)
        self.add_message("assistant", response)
        return {"response": response}

    async def query(self, question: str) -> str:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=self.default_prompt + question,
            max_tokens=150
        )
        return response.choices[0].text.strip()
