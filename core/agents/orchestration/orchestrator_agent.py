import uuid
from core.agent import Agent
from core.utils.db_interactions import DatabaseClient

class Orchestrator:
    def __init__(self):
        self.db_client = DatabaseClient()

    # Search for an existing agent in the database by task or create a new one
    async def find_or_create_agent(self, task_name, agent_config):
        """
        Find an agent capable of performing the given task, or create one.        
        """
        # Search for an agent capable of the task
        capable_agent = self.db_client.find_agent_by_task(task_name)
        
        if capable_agent:
            print(f"Found an agent capable of {task_name}: {capable_agent.agent_name}")
            return capable_agent
        else:
            # No capable agent found, so create a new one
            new_agent_id = str(uuid.uuid4())
            new_agent = Agent(new_agent_id, agent_config["agent_name"], tools=agent_config.get("tools", []))
            print(f"Creating new agent for task {task_name} with ID {new_agent_id}")
            
            # Save the new agent in the database
            self.db_client.save_agent(new_agent)
            
            return new_agent

    def get_next_task(self, tasks, context):
        """
        Get the next task that is ready to be executed based on dependencies.
        """
        for task_name, task_info in tasks.items():
            if self.are_dependencies_met(task_info, context):
                return task_name, task_info
        return None, None

    def are_dependencies_met(self, task_info, context):
        """
        Check if the task's dependencies are met.
        """
        dependencies = task_info.get("dependencies", [])
        for dep in dependencies:
            if context.get_state(dep) != "completed":
                return False
        return True

    async def execute(self, process, context):
        """
        Facilitates the execution of the workflow, dynamically creating and assigning agents.
        """
        tasks = process.workflow["tasks"]

        while tasks:
            # Fetch the next task that is ready to be executed
            task_name, task_info = self.get_next_task(tasks, context)
            if not task_name:
                print("No tasks ready to execute, waiting for dependencies.")
                break

            agent_config = task_info.get("agent_config")
            agent = await self.create_or_load_agent(agent_config)
            
            # Delegate the task to the agent
            result = await agent.execute_task(task_info["action"], task_info.get("input_data", {}))
            
            # Save task results and update context
            self.db_client.save_task({
                "agent_id": agent.agent_id,
                "task_name": task_name,
                "task_status": "completed" if result else "failed",
                "result": result
            })
            
            context.update_state(task_name, result)
            print(f"Task {task_name} executed by agent {agent.agent_id} with result: {result}")
            
            # Remove the executed task from the task list
            tasks.pop(task_name)
            
    def get_tools_for_task(self, task_id):
        query = "SELECT tool_name FROM tools t JOIN task_tools tt ON t.tool_id = tt.tool_id WHERE tt.task_id = ?"
        return self.execute_query(query, [task_id])