import logging
from typing import Dict, Any, List
from core.decorators.retry import Retry
from core.execution_context import ExecutionContext

class Orchestrator:
    @Retry.retry_on_exception(max_retries=3, delay=2, exceptions=(Exception,))
    async def execute(self, process, context):
        """
        Facilitates the execution of the workflow.
        Receives the workflow from the Process instance and executes tasks based on dependencies.
        """
        logging.info("Executing workflow...")
        
        # Get the agents from the process
        self.agents = process.agents
        
        # Get the starting task from the process
        current_task = process.get_start_task()  # Use the get_start_task method to get the first task

        while current_task:
            # Access the workflow's tasks properly
            task_info = process.workflow["tasks"][current_task]  # Correctly access the tasks dictionary
            agent = self.agents[task_info["agent"]]
            action = task_info["action"]
            input_data = task_info.get("input_data", {})

            # Execute the action asynchronously
            result = await agent._execute_task_async(action, input_data)
            context.update_state(current_task, result)

            # Handle task-specific completion actions if they exist
            if hasattr(context, "handle_" + action):
                handle_method = getattr(context, "handle_" + action)
                handle_method(result)

            # Get the next task based on workflow completion and dependencies
            current_task = self.get_next_task(process.workflow, context)

    def get_next_task(self, workflow, context):
        """
        Retrieve the next task in the workflow based on completed tasks and dependencies.
        """
        for task_name, task_info in workflow["tasks"].items():
            if task_name not in context.completed_tasks and self.are_dependencies_met(task_info, context):
                return task_name
        return None


