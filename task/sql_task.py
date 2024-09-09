from typing import List
from core.tasks.base_task import TaskBase
from agent.sql.sql_agent import SQLAgent

class SQLTask(TaskBase):
    def __init__(self, name: str, description: str, tools: List[str], action: str, dependencies=None):
        super().__init__(name, description, tools, dependencies)
        self.action = action
        self.agent = SQLAgent()

    async def run(self) -> any:
        # You can now dynamically execute any known action
        if self.action == "generate_sql":
            return await self.agent.execute_sql_action("generate_sql", natural_language_query=self.context["query"])
        elif self.action == "run_sql_return_rows":
            return await self.agent.execute_sql_action("run_sql_return_rows", sql_query=self.context["sql_query"], database_path=self.context["db_path"])
        elif self.action == "validate_sql":
            return await self.agent.execute_sql_action("validate_sql", sql_query=self.context["sql_query"])
        else:
            raise ValueError(f"Unknown action: {self.action}")
