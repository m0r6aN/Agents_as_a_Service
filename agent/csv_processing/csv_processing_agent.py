# core/agents/specialized_agents.py

from .base_agent import BaseAgent
from ..system_messages.specialized_messages import CSV_PROCESSING_MESSAGE
from ..prompts.specialized_prompts import CSV_ANALYSIS_PROMPT
from ..actions.file_actions import get_file_info, read_file_content
from ..actions.data_actions import analyze_csv
from ..tools.file_utils import get_file_hash
from ..tools.data_processing import detect_outliers

class CSVProcessingAgent(BaseAgent):
    def __init__(self):
        known_actions = {
            "get_file_info": get_file_info,
            "read_file_content": read_file_content,
            "analyze_csv": analyze_csv,
            "get_file_hash": get_file_hash,
            "detect_outliers": detect_outliers,
        }
        super().__init__(
            known_actions=known_actions,
            default_prompt=CSV_ANALYSIS_PROMPT,
            system_message=CSV_PROCESSING_MESSAGE
        )

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        file_path = input_data["file_path"]
        file_info = self.run_action("get_file_info", file_path)
        csv_analysis = self.run_action("analyze_csv", file_path)
        
        prompt = self.default_prompt.format(**file_info)
        self.add_message("user", prompt)
        
        # Here you would typically send the messages to an LLM and get a response
        # For this example, we'll just return the analysis
        return {
            "file_info": file_info,
            "csv_analysis": csv_analysis,
            "file_hash": self.run_action("get_file_hash", file_path)
        }

    async def query(self, question: str) -> str:
        self.add_message("user", question)
        # Here you would typically send the messages to an LLM and get a response
        # For this example, we'll just return a placeholder
        return "This is a placeholder response to your query."