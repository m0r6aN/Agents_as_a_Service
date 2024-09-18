# agents/specialized_agents/specialized_agent.py

import logging
from agents.agent_base import Agent
from tools.default_tools import online_search, memory, communication, code_execution, prompt_generation

class SpecializedAgent(Agent):
    def __init__(self, agent_name, system_message, model_name, tools=None, memory=None, config=None):
        super().__init__(agent_name, system_message, model_name, tools, memory, config)
        self.logger = logging.getLogger(self.agent_name)

    def perform_task(self, task):
        self.logger.info(f"Starting task {task.task_id}: {task.task_name}")
        try:
            # Check for dependencies
            if task.dependencies:
                self.handle_dependencies(task.dependencies)
            # Execute the task function
            result = task.function()
            task.status = 'COMPLETED'
            self.logger.info(f"Task {task.task_id} completed successfully.")
            self.report_to_superior(result)
        except Exception as e:
            task.status = 'FAILED'
            self.logger.error(f"Task {task.task_id} failed: {str(e)}")
            if task.retry_count > 0:
                task.retry_count -= 1
                self.perform_task(task)
            else:
                self.report_failure(e)

    def handle_dependencies(self, dependencies):
        for dependency in dependencies:
            # Logic to check and wait for dependencies to complete
            self.logger.debug(f"Handling dependency: {dependency}")
            pass

    def create_tool(self, tool_name, tool_description, function):
        tool_id = str(uuid.uuid4())
        tool_data = {
            'tool_id': tool_id,
            'tool_name': tool_name,
            'tool_description': tool_description,
            'version': '1.0',
            'function': function
        }
        self.db.save_tool(tool_data)
        self.tools.append(tool_id)
        self.db.update_agent_tools(self.agent_id, self.tools)
        self.logger.info(f"New tool created and added: {tool_name} (ID: {tool_id})")

    def report_to_superior(self, result):
        message = f"Task completed with result: {result}"
        self.communicate(message, self.config.get('superior_agent_id'))
        self.logger.debug(f"Reported to superior: {message}")

    def report_failure(self, error):
        message = f"Task failed with error: {error}"
        self.communicate(message, self.config.get('superior_agent_id'))
        self.logger.debug(f"Reported failure to superior: {message}")
