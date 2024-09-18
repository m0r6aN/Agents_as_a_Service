# agents/orchestrator/orchestrator.py

import json
import logging
from config.settings import DATABASE, MESSAGE_BROKER, AGENT_DEFAULTS
from agents.agent_base import Agent
from agents.core_agents.prompt_agent.prompt_agent import PromptAgent
from agents.specialized_agents.specialized_agent import SpecializedAgent
from agents.task import Task

class OrchestratorAgent(Agent):
    def __init__(self):
        super().__init__(
            agent_name="Orchestrator",
            system_message="",
            model_name="GPT-4",
            tools=None
        )
        self.logger = logging.getLogger(self.agent_name)
        self.prompt_agent = PromptAgent()

    def receive_message(self, message):
        self.logger.debug(f"Process request received: {message}")
        process_request = json.loads(message)
        self.handle_process_request(process_request)

    def handle_process_request(self, process_request):
        tasks = process_request.get('tasks', [])
        for task_data in tasks:
            task = Task(**task_data)
            self.assign_task(task, process_request['process_id'])

    def assign_task(self, task, process_id):
        # Find agent with the required capabilities
        agent_data = self.db.find_agent_by_capabilities(task.capabilities)
        if not agent_data:
            # Create a new agent or handle as appropriate
            agent = self.create_agent_for_task(task)
        else:
            agent = self.load_agent_from_data(agent_data)

        # Prepare task message
        task_message = {
            'process_id': process_id,
            'task': task.__dict__
        }
        # Send task to the TaskScheduler
        self.messaging_client.send_message('task_scheduler', json.dumps(task_message))
        self.logger.info(f"Task {task.task_id} assigned to TaskScheduler.")

    def generate_system_prompt(self, task):
        system_prompt = self.prompt_agent.generate_prompt(task)
        self.logger.debug(f"System prompt generated: {system_prompt}")
        return system_prompt

    def load_agent_from_data(self, agent_data):
        agent = SpecializedAgent(
            agent_name=agent_data['agent_name'],
            system_message=agent_data['system_message'],
            model_name=agent_data['model_name'],
            tools=agent_data['tools'],
            memory=agent_data['memory'],
            config=agent_data['config']
        )
        return agent
