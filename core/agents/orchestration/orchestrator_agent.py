# agents_as_a_service/core/agents/orchestration/orchestrator_agent.py

import logging
from core.agent import Agent
from core.utils.task_handler import TaskHandler

class Orchestrator:
    def __init__(self):
        self.db = DatabaseClient()  # For storing agent configurations dynamically

    async def create_or_load_agent(self, agent_config):
        """
        Either load an existing agent from the database or create a new one dynamically.
        """
        agent_id = agent_config.get("id")
        if agent_id and self.db.agent_exists(agent_id):
            # Load existing agent
            agent = Agent(agent_name="")
            agent.load_agent(agent_id)
        else:
            # Create a new dynamic agent
            agent = Agent(agent_name=agent_config["name"], tools=agent_config.get("tools"))
            agent.save_agent()  # Save the new agent to the database
        
        return agent

    async def execute(self, process, context):
        """
        Facilitates the execution of the workflow, dynamically creating and assigning agents.
        """
        # Get the tasks from the process
        tasks = process.workflow["tasks"]

        for task_name, task_info in tasks.items():
            # Dynamically create or load an agent
            agent_config = task_info.get("agent_config")
            agent = await self.create_or_load_agent(agent_config)
            
            # Delegate the task to the agent
            result = await agent.execute_task(task_info["action"], task_info.get("input_data", {}))
            context.update_state(task_name, result)
            
    def get_next_task(self, workflow, context):
        """
        Retrieve the next task in the workflow based on completed tasks and dependencies.
        """
        for task_name, task_info in workflow["tasks"].items():
            if task_name not in context.completed_tasks and self.are_dependencies_met(task_info, context):
                return task_name
        return None

    def are_dependencies_met(self, task_info, context):
        return all(dep in context.completed_tasks for dep in task_info.get('dependencies', []))