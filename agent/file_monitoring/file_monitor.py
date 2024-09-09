import logging
from typing import Dict, Any
import pika
from agents.base_agent import BaseAgent

logging.basicConfig(level=logging.INFO)

class FileMonitorAgent(BaseAgent):
    def __init__(self, config: Dict[str, Any]):
        known_actions = {
            'monitor_files': self.monitor_files
        }
        default_prompt = "Monitor files for changes."
        super().__init__(known_actions, default_prompt, system_message="File Monitor Agent Initialized", max_turns=5)
        self.config = config

    async def _execute_task(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform the file monitoring task using the input data.
        """
        # Simulate monitoring files (you would implement the actual monitoring logic here)
        self.log_action("Started file monitoring.")
        self.monitor_files()
        self.log_action("Completed file monitoring.")
        return {"status": "success", "message": "Files monitored successfully"}

    async def query(self, question: str) -> str:
        """
        Handle any queries directed at the FileMonitorAgent.
        """
        # For now, we'll just return a default response
        return f"FileMonitorAgent received the question: {question}"

    def monitor_files(self):
        """
        Placeholder function to simulate file monitoring.
        """
        print("Monitoring files...")

    def callback(self, ch, method, properties, body):
        """
        Handle incoming messages from the service bus.
        """
        logging.info(f"Received {body}")
        try:
            result = self.execute(body)  # Assuming body is a serialized dict of input_data
            logging.info(f"Task executed with result: {result}")
        except Exception as e:
            logging.error(f"Error executing task: {str(e)}")

# Example of how to instantiate and connect the agent to the service bus

if __name__ == "__main__":
    # Example configuration
    config = {
        "monitor_interval": 10  # Just an example config parameter
    }

    agent = FileMonitorAgent(config)

    # Connect to RabbitMQ and start listening for tasks
    agent.connect_service_bus(queue_name='file_monitor', service_bus=None)  # Assuming service_bus is defined elsewhere
