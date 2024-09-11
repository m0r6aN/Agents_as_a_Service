# agents_as_a_service/core/utils/task_handler.py

from core.utils.retry_utils import Retry
import logging

class TaskHandler:
    
    @Retry.retry_on_exception(max_retries=3, delay=2, exceptions=(Exception,))
    async def execute_task(self, agent, action, input_data):
        """
        Executes a task asynchronously using the specified agent.
        Handles retries via decorator.
        """
        logging.info(f"Executing task {action} for agent {agent.agent_name}...")
        result = await agent._execute_task_async(action, input_data)
        logging.info(f"Task {action} for agent {agent.agent_name} completed with result: {result}")
        return result
