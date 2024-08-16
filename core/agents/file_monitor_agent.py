# File: agents_as_a_service/core/agents/file_monitor_agent.py

from .base_agent import BaseAgent
from ..actions.file_actions import get_file_info
from ..actions.gcp_actions import validate_csv_ai
from ..tools.file_tools import get_file_hash

class FileMonitorAgent(BaseAgent):
    def __init__(self, config):
        known_actions = {
            "get_file_info": get_file_info,
            "get_file_hash": get_file_hash,
            "validate_csv_ai": validate_csv_ai
        }
        super().__init__(
            known_actions=known_actions,
            default_prompt="Monitor and validate the following file: {file_path}",
            system_message="You are a file monitoring agent capable of detecting changes and validating CSV files using AI."
        )
        self.config = config

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        file_path = input_data["file_path"]
        file_info = self.run_action("get_file_info", file_path)
        file_hash = self.run_action("get_file_hash", file_path)
        
        if file_info["filename"].endswith('.csv'):
            validation_result = self.run_action("validate_csv_ai", self.config["bucket_name"], file_info["filename"])
        else:
            validation_result = {"message": "Not a CSV file, skipping AI validation."}
        
        return {
            "file_info": file_info,
            "file_hash": file_hash,
            "validation_result": validation_result
        }