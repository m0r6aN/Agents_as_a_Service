from abc import ABC, abstractmethod
import logging
from typing import Dict, List, Callable, Optional
from functools import wraps
import sys, os
from abc import ABC, abstractmethod
import logging
from typing import Dict, Callable, Optional, List

# Add the path to the root directory of the project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.decorators.retry import Retry

class BaseAgent(ABC):
    def __init__(self, known_actions: Dict[str, Callable], logger: Optional[logging.Logger] = None, tools: Optional[List] = None):
        """
        Initialize the BaseAgent with known actions and dependencies.
        
        :param known_actions: A dictionary of actions this agent can perform.
        :param logger: Injected logger instance for logging.
        :param tools: Injected list of tools the agent can use.
        """
        self.known_actions = known_actions
        self.state = "idle"  # Default state is idle
        self.logger = logger or logging.getLogger(__name__)
        self.tools = tools or []  # Use injected tools or an empty list

    @abstractmethod
    @Retry.retry_on_exception(max_retries=3, delay=2, exceptions=(Exception,))
    async def execute_async(self, input_data: Dict[str, any]) -> Dict[str, any]:
        """
        Execute the agent's main function using the input data.
        
        :param input_data: The input data required for execution.
        :return: The output data after execution.
        """
        self.state = "processing"
        result = await self._execute_task(input_data)
        self.state = "idle"
        return result
    
    @abstractmethod
    async def _execute_task_async(self, input_data: Dict[str, any]) -> Dict[str, any]:
        """
        Sub-method to actually perform the task, allowing for pre- and post-execution hooks.
        """
        pass

    async def execute_action(self, action_name: str, **kwargs):
        if action_name not in self.known_actions:
            raise ValueError(f"Action {action_name} is not recognized.")
        
        action = self.known_actions[action_name]
        return await action(**kwargs)

    def use_tool(self, tool_name: str, *args, **kwargs) -> any:
        tool = next((tool for tool in self.tools if tool.name == tool_name), None)
        if tool is None:
            raise ValueError(f"Tool {tool_name} not found.")
        
        return tool.execute(*args, **kwargs)

    def load_tool(self, tool_class, *args, **kwargs):
        """
        Dynamically load a tool if it is not already loaded.
        """
        tool_instance = tool_class(*args, **kwargs)
        self.tools.append(tool_instance)
        self.logger.info(f"Loaded tool {tool_class.__name__}.")

    def log_action(self, action: str):
        """
        Log an action performed by the agent using the injected logger.
        
        :param action: A string describing the action performed.
        """
        self.logger.info(f"{self.__class__.__name__} performed action: {action}")

    def reset(self):
        """
        Reset the agent's state.
        """
        self.state = "idle"
        self.logger.info(f"{self.__class__.__name__} state has been reset to idle.")

