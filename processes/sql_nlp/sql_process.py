from agent.sql.sql_agent import SQLAgent

from core.process.process_base import ProcessBase
from task.sql_task import SQLTask

class SQLProcess(ProcessBase):
    def define_agents(self):
        sql_agent = SQLAgent()
        # another_agent = SomeOtherAgent()
        
        self.agents = {
            "sql_agent": sql_agent,
           # "another_agent": another_agent
        }

    def define_tasks(self):
        generate_sql_task = SQLTask(
            name="Generate SQL",
            description="Convert natural language to SQL",
            tools=["sql_tool"],
            action="generate_sql"
        )
    
        validate_sql_task = SQLTask(
            name="Validate SQL",
            description="Ensure the SQL query is safe",
            tools=["sql_tool"],
            action="validate_sql",
            dependencies=[generate_sql_task]
        )
        
        execute_sql_task = SQLTask(
            name="Execute SQL",
            description="Run the SQL query on the database",
            tools=["db_tool"],
            action="run_sql_return_rows",
            dependencies=[validate_sql_task]
        )

        self.add_task(generate_sql_task)
        self.add_task(validate_sql_task)
        self.add_task(execute_sql_task)

    def define_workflow(self):
        self.workflow = {
            "start": "task1",  # The first task in the workflow
            "tasks": {
                "task1": {
                    "agent": "sql_agent",
                    "action": "generate_sql",
                    "input_data": {"natural_language_query": "Show me all customers from the USA."},
                },
                "task2": {
                    "agent": "sql_agent",
                    "action": "execute_sql",
                    "dependencies": ["task1"]
                }
            }
        }
        
    def get_start_task(self):
        return self.workflow.get("start")  # This method retrieves the first task

    def handle_sql_generation(self, query_result):
        # Called after SQL query is generated
        self.logger.info(f"SQL Query Generated: {query_result}")
        # Update workflow to pass the generated query into the execution task
        self.modify_workflow({
            "task2": {
                "input_data": {"sql_query": query_result}
            }
        })
