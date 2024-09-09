import logging

from core.base_agent import BaseAgent
from core.actions.sqlite_actions import (
    run_sql_return_csv,
    run_sql_return_rows,
    validate_sql,
    generate_sql,
)

class SQLAgent(BaseAgent):
    def __init__(self, logger: logging.Logger = None):
        known_actions = {
            "run_sql_return_csv": run_sql_return_csv,
            "run_sql_return_rows": run_sql_return_rows,
            "validate_sql": validate_sql,
            "generate_sql": generate_sql,
        }
        super().__init__(known_actions, logger)
        
    async def _execute_task_async(self, action_name, input_data):
        """
        Executes a task asynchronously using the action name and input data.
        
        :param action_name: The name of the action to perform (e.g., "generate_sql").
        :param input_data: The input data required for the action.
        :return: The result of the action.
        """
        if action_name not in self.known_actions:
            raise ValueError(f"Unknown action: {action_name}")
        
        # Call the action dynamically with the input_data
        return await self.known_actions[action_name](**input_data)

    # Placeholder for abstract method 2
    async def execute_async(self, *args, **kwargs):
        # Implement your logic or leave as pass
        pass
