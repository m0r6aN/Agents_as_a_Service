# File: processes/file_processing/custom_agents.py

from agent import BaseAgent
import os
import csv
from typing import Dict, Any

# Example storage monitoring agent.
# Monitors input directory for new files
class FileMonitorAgent(BaseAgent):
    def __init__(self, config):
        super().__init__("File Monitor", "Monitors input directory for new files")
        self.input_directory = config["input_directory"]
        self.file_types = config["file_types"]

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        files = [f for f in os.listdir(self.input_directory) if f.split('.')[-1] in self.file_types]
        return {"files": files}

# Example file processing agent.
# Processes files and performs word count
class FileProcessorAgent(BaseAgent):
    def __init__(self, config):
        super().__init__("File Processor", "Processes files and performs word count")
        self.input_directory = config["input_directory"]
        self.output_directory = config["output_directory"]

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        files = input_data["files"]
        results = {}
        for file in files:
            word_count = self._process_file(file)
            results[file] = word_count
        return {"processed_files": results}

    def _process_file(self, filename):
        with open(os.path.join(self.input_directory, filename), 'r') as file:
            content = file.read()
            return len(content.split())

# Example result writer agent
# Writes processing results to output file
class ResultWriterAgent(BaseAgent):
    def __init__(self, config):
        super().__init__("Result Writer", "Writes processing results to output file")
        self.output_directory = config["output_directory"]

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        processed_files = input_data["processed_files"]
        output_file = os.path.join(self.output_directory, "word_counts.csv")
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Filename", "Word Count"])
            for filename, count in processed_files.items():
                writer.writerow([filename, count])
        return {"output_file": output_file}
    
