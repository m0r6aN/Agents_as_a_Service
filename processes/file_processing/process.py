# File: processes/file_processing/process.py

from core import ProcessBase
from custom_agents import FileMonitorAgent, FileProcessorAgent, ResultWriterAgent

class FileProcessingProcess(ProcessBase):
    def __init__(self, config):
        super().__init__("File Processing", "Process files and count words", config)
        self.define_agents()
        self.define_workflow()

    def define_agents(self):
        # Core agents (MonitoringAgent and LoggingAgent) are already added in ProcessBase
        self.add_agent(FileMonitorAgent(self.config))
        self.add_agent(FileProcessorAgent(self.config))
        self.add_agent(ResultWriterAgent(self.config))

    def define_workflow(self):
        self.set_workflow({
            "tasks": {
                # MonitoringAgent and LoggingAgent tasks are automatically added by set_workflow
                "file_monitor": {"agent": "FileMonitorAgent", "dependencies": ["monitoring", "logging"]},
                "file_processor": {"agent": "FileProcessorAgent", "dependencies": ["file_monitor"]},
                "result_writer": {"agent": "ResultWriterAgent", "dependencies": ["file_processor"]}
            }
        })