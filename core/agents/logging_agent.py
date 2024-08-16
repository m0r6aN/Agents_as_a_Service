# File: multi_agent_framework/core/agents/logging_agent.py

import logging
from .base import BaseAgent
from typing import Dict, Any

class LoggingAgent(BaseAgent):
    def __init__(self, log_file: str, log_level: int = logging.INFO):
        super().__init__("Logging Agent", "Handles logging for the process")
        logging.basicConfig(filename=log_file, level=log_level, 
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('ProcessLogger')

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in input_data.items():
            self.logger.info(f"{key}: {value}")
        return {"logging": "completed"}

    def log_error(self, error_message: str):
        self.logger.error(error_message)

    def log_info(self, info_message: str):
        self.logger.info(info_message)
