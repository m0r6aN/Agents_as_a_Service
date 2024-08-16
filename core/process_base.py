from abc import ABC, abstractmethod
from typing import List, Dict, Any
from agents import BaseAgent
from agents.monitoring_agent import MonitoringAgent
from agents.logging_agent import LoggingAgent

class ProcessBase(ABC):
    def __init__(self, name: str, description: str, config: Dict[str, Any]):
        self.name = name
        self.description = description
        self.config = config
        self.agents: List[BaseAgent] = []
        self.workflow: Dict[str, Any] = {}
        
        # Add core agents
        self.add_agent(MonitoringAgent())
        self.add_agent(LoggingAgent(config.get('log_file', f"{name.lower().replace(' ', '_')}.log")))

    def add_agent(self, agent: BaseAgent):
        self.agents.append(agent)

    @abstractmethod
    def define_agents(self):
        pass

    @abstractmethod
    def define_workflow(self):
        pass

    def set_workflow(self, workflow: Dict[str, Any]):
        # Ensure monitoring and logging are always first in the workflow
        core_tasks = {
            "monitoring": {"agent": "MonitoringAgent", "dependencies": []},
            "logging": {"agent": "LoggingAgent", "dependencies": []}
        }
        workflow["tasks"] = {**core_tasks, **workflow["tasks"]}
        self.workflow = workflow