# agents/agent_base.py

import uuid
import logging
from abc import ABC, abstractmethod
from agents.specialized_agents.specialized_agent import SpecializedAgent
from messaging.messaging import MessagingClient
from database.database_setup import Database

class Agent(ABC):
    def __init__(self, agent_name, system_message, model_name, tools=None, memory=None, config=None):
        self.agent_id = str(uuid.uuid4())
        self.agent_name = agent_name
        self.system_message = system_message
        self.model_name = model_name
        self.tools = tools if tools else []
        self.memory = memory if memory else {}
        self.config = config if config else {}
        self.messaging_client = MessagingClient()
        self.db = Database()
        self.logger = logging.getLogger(self.agent_name)
        self.persist_agent()

    def persist_agent(self):
        agent_data = {
            'agent_id': self.agent_id,
            'agent_name': self.agent_name,
            'system_message': self.system_message,
            'model_name': self.model_name,
            'tools': self.tools,
            'memory': self.memory,
            'config': self.config
        }
        self.db.save_agent(agent_data)
        self.logger.debug(f"Agent {self.agent_id} persisted to database.")

    @abstractmethod
    def perform_task(self, task):
        pass

    def communicate(self, message, recipient_agent_id):
        self.messaging_client.send_message(recipient_agent_id, message)
        self.logger.debug(f"Message sent to {recipient_agent_id}: {message}")

    def receive_message(self, message):
        self.logger.debug(f"Message received: {message}")
        # Process received message
        pass

    def create_sub_agent(self, agent_name, system_message, model_name, tools=None):
        sub_agent = SpecializedAgent(agent_name, system_message, model_name, tools)
        self.logger.debug(f"Sub-agent created: {sub_agent.agent_id}")
        return sub_agent

    def save_to_memory(self, key, value):
        self.memory[key] = value
        self.db.update_agent_memory(self.agent_id, self.memory)
        self.logger.debug(f"Memory updated for {self.agent_id}: {key} = {value}")
        
    def report_status_to_superior(self, taskid, status):
        """
        Reports task status to the superior agent or logs it appropriately.
        """
        message = f"Task status for {taskid}: {status}"
        self.communicate(message, self.config.get('superior_agent_id'))
        self.logger.debug(f"Reported to superior: {message}")
        
    def report_completion(self, info):
        """
        Reports failure to the superior agent or logs it appropriately.
        """
        message = f"Task completed with message: {info}"
        if self.config.get('superior_agent_id'):
            self.communicate(message, self.config.get('superior_agent_id'))
            self.logger.debug(f"Reported failure to superior: {message}")
        else:
            self.logger.error(message)
        
    def report_failure(self, error):
        """
        Reports failure to the superior agent or logs it appropriately.
        """
        message = f"Task failed with error: {error}"
        if self.config.get('superior_agent_id'):
            self.communicate(message, self.config.get('superior_agent_id'))
            self.logger.debug(f"Reported failure to superior: {message}")
        else:
            self.logger.error(message)