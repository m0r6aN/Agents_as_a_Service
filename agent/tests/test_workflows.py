import asyncio
import sys
import os
from typing import Dict

# Add the path to the 'agents' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Add the path to the root directory of the project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agents.notification.notification_agent import NotificationAgent
from agents.processing.processing_agent import ProcessingAgent

from base_agent import BaseAgent
from execution_context import ExecutionContext

# Set up a simple logger
import logging
logging.basicConfig(level=logging.INFO)

class TestAgent(BaseAgent):
    async def run_action(self, action: str, input_data: Dict[str, any]) -> Dict[str, any]:
        self.logger.info(f"Running action: {action}")
        # Simulate a task that just returns a message
        await asyncio.sleep(1)
        return {f"result_of_{action}": f"Executed {action}"}

    async def _execute_task_async(self, task_name: str, input_data: Dict[str, any]) -> Dict[str, any]:
        # Placeholder implementation
        self.logger.info(f"Executing task: {task_name} with input {input_data}")
        await asyncio.sleep(1)  # Simulate some work
        return {f"result_of_{task_name}": f"Executed {task_name}"}

    async def execute_async(self, input_data: Dict[str, any]) -> Dict[str, any]:
        # Placeholder implementation
        self.logger.info(f"Executing workflow with input {input_data}")
        await asyncio.sleep(1)  # Simulate some work
        return {"result": "workflow executed"}

    async def query_async(self, question: str) -> str:
        # Placeholder implementation
        return f"Query received: {question}"

    # Override on_message to handle incoming messages
    def on_message(self, ch, method, properties, body):
        super().on_message(ch, method, properties, body)
        # Example: Decode and process the message
        message = body.decode()
        self.logger.info(f"TestAgent received: {message}")
        # Perform some action based on the message if necessary

async def test_complex_workflow():
    # Initialize agents
    test_agent = TestAgent(known_actions={}, default_prompt="Test", system_message="Testing")
    processing_agent = ProcessingAgent(known_actions={}, default_prompt="Process", system_message="Processing Task")
    notification_agent = NotificationAgent(known_actions={}, default_prompt="Notify", system_message="Sending Notifications")

    # Register agents
    test_agent.register_agent("ProcessingAgent", processing_agent)
    test_agent.register_agent("NotificationAgent", notification_agent)

    # Define the workflow
    complex_workflow = {
        "start": "Task A",
        "tasks": {
            "Task A": {"task": {"agent": "TestAgent", "action": "Start Process"}, "next": "Task B"},
            "Task B": {"task": {"agent": "ProcessingAgent", "action": "Process Data"}, "next": "Task C"},
            "Task C": {"task": {"agent": "NotificationAgent", "action": "Send Notification"}, "next": None}
        }
    }

    # Execute the complex workflow
    results = await test_agent.execute_linear_workflow_async(complex_workflow, input_data={})
    
    # Output the results
    print("Complex Workflow Results:", results)

    # Start listening for messages in each agent
    test_agent.start_listening()
    processing_agent.start_listening()
    notification_agent.start_listening()


# Run the test
asyncio.run(test_complex_workflow())