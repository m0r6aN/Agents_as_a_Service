from abc import ABC, abstractmethod
import logging

from core.execution_context import ExecutionContext

class ProcessBase(ABC):
    def __init__(self, orchestrator):
        """
        Initializes the Process instance class.
        """
        self.orchestrator = orchestrator
        self.agents = []
        self.tasks = []
        self.workflow = {}
        self.context = ExecutionContext()
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def define_agents(self):
        """
        Defines the agents involved in the workflow. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def define_tasks(self):
        """
        Defines the tasks required for the workflow. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def define_workflow(self):
        """
        Defines the workflow, including the sequence and parallel execution of agents and tasks. Must be implemented by subclasses.
        """
        pass
    
    def modify_workflow(self, modifications: dict):
        """
        Modify the workflow dynamically, allowing tasks to be added or removed based on conditions.
        """
        for task, changes in modifications.items():
            if task in self.workflow:
                self.workflow[task].update(changes)
            else:
                self.workflow[task] = changes
                
    def get_start_task(self):
        """
        Returns the start task of the workflow.
        This method assumes there is a task marked as 'start'.
        """
        return self.workflow.get("start")

    def add_agent(self, agent):
        """
        Adds an agent to the workflow.
        """
        self.agents.append(agent)

    def add_task(self, task, dependencies=None):
        """
        Adds a task to the workflow with optional dependencies.
        """
        self.tasks.append({"task": task, "dependencies": dependencies or []})

    def set_workflow(self, workflow):
        """
        Sets the workflow for the process.
        """
        self.workflow = workflow

    def __repr__(self):
        return f"<ProcessBase agents={self.agents}, tasks={self.tasks}, workflow={self.workflow}>"
