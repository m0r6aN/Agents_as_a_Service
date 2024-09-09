from core import ProcessBase
from custom_agents import FileMonitorAgent, FileProcessorAgent, ResultWriterAgent

class FileProcessingProcess(ProcessBase):
    def __init__(self, config):
        super().__init__("File Processing", "Process files and count words", config)
        self.define_agents()
        self.define_workflow()

    def define_agents(self):
        """
        Defines all agents required for the process and adds them to the process.
        """
        # Core agents (MonitoringAgent and LoggingAgent) are already added in ProcessBase
        self.add_agent(FileMonitorAgent(self.config))
        self.add_agent(FileProcessorAgent(self.config))
        self.add_agent(ResultWriterAgent(self.config))

    def define_workflow(self):
        """
        Defines the process workflow, where tasks are dependent on each other.
        """
        self.set_workflow({
            "tasks": {
                # Core agents' tasks (monitoring, logging) are included from ProcessBase
                "file_monitor": {"agent": "FileMonitorAgent", "dependencies": ["monitoring", "logging"]},
                "file_processor": {"agent": "FileProcessorAgent", "dependencies": ["file_monitor"]},
                "result_writer": {"agent": "ResultWriterAgent", "dependencies": ["file_processor"]}
            }
        })
    
    def execute(self):
        """
        Execute the process step-by-step while handling task dependencies.
        """
        try:
            self.orchestrator.start_process(self.workflow)
        except Exception as e:
            self.orchestrator.handle_failure(f"Process failed: {e}")
