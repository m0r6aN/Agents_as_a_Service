from agents.agent_base import Agent
from typing import Any, Dict, List

class SpecializedAgent(Agent):
    def __init__(self, agent_name: str, system_message: str, model_name: str, tools: List[str] = None, memory: Dict[str, Any] = None, config: Dict[str, Any] = None):
        super().__init__(agent_name, system_message, model_name, tools, memory, config)

    def perform_task(self, task: Any) -> Any:
        self.logger.info(f"Starting task {task.task_id}: {task.task_name}")
        try:
            # Check for dependencies
            if task.dependencies:
                self.handle_dependencies(task.dependencies)

            # Check if a tool is needed
            if task.requires_tool:
                tool_id = self.find_or_create_tool(
                    task.tool_name,
                    task.tool_description,
                    task.tool_code
                )
                result = self.execute_tool(tool_id, *task.args, **task.kwargs)
            else:
                # Execute the task function
                result = task.function()

            self.report_status(task.task_id, 'COMPLETED')
            self.logger.info(f"Task {task.task_id} completed successfully.")
            self.report_completion(task.task_id, result)
            return result
        except Exception as e:
            self.report_status(task.task_id, 'FAILED')
            self.logger.error(f"Task {task.task_id} failed: {str(e)}")
            if task.retry_count > 0:
                task.retry_count -= 1
                return self.perform_task(task)
            else:
                self.report_failure(task.task_id, str(e))
                raise

    def handle_dependencies(self, dependencies: List[Any]) -> None:
        for dependency in dependencies:
            # Logic to check and wait for dependencies to complete
            self.logger.debug(f"Handling dependency: {dependency}")
            # Implement actual dependency handling logic here