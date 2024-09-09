# File: core/tools/base_tool.py

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict
import logging

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """
    Abstract base class for all tools.
    """

    def __init__(self, name: str, description: str, function: Callable, version: str = "1.0"):
        self.name = name
        self.description = description
        self.version = version
        self.function = function

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the tool's function with the given arguments.
        
        :param args: Positional arguments for the tool's function.
        :param kwargs: Keyword arguments for the tool's function.
        :return: The result of the tool's function execution.
        """
        return self.function(*args, **kwargs)

    def __repr__(self):
        return f"<Tool name={self.name} version={self.version}>"
