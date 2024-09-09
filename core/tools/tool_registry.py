# File: core/tools/tool_registry.py

from typing import Dict, Type
from tool_base import BaseTool

class ToolRegistry:
    """
    Registry for managing and retrieving tools.
    """

    _registry: Dict[str, BaseTool] = {}

    @classmethod
    def register_tool(cls, tool: BaseTool):
        cls._registry[tool.name] = tool

    @classmethod
    def get_tool(cls, name: str) -> BaseTool:
        tool = cls._registry.get(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found in registry.")
        return tool

    @classmethod
    def list_tools(cls) -> Dict[str, BaseTool]:
        return cls._registry

# Registering tools
from core.tools.web_scraper_tool import WebScraperTool

ToolRegistry.register_tool(WebScraperTool())
