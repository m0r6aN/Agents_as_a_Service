# File: multi_agent_framework/core/agents/monitoring_agent.py

import psutil
from .base_agent import BaseAgent
from typing import Dict, Any

class MonitoringAgent(BaseAgent):
    def __init__(self):
        super().__init__("Monitoring Agent", "Monitors system resources")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage
        }
