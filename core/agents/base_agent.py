# File: multi_agent_framework/agents/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable

class BaseAgent(ABC):
    paused = False
    streaming_agent = None

    def __init__(self, known_actions: Dict[str, Callable], default_prompt: str, system_message: str = "", max_turns: int = 5):
        self.known_actions = known_actions
        self.default_prompt = default_prompt
        self.system_message = system_message
        self.max_turns = max_turns
        self.messages: List[Dict[str, str]] = []
        if self.system_message:
            self.messages.append({"role": "system", "content": self.system_message})

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def query(self, question: str) -> str:
        pass

    def run_action(self, action: str, action_input: Any) -> Any:
        if action not in self.known_actions:
            raise ValueError(f"Unknown action: {action}")
        return self.known_actions[action](action_input)

    def reset(self):
        self.messages = []
        if self.system_message:
            self.messages.append({"role": "system", "content": self.system_message})