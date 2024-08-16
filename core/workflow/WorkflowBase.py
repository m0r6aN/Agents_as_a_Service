from abc import ABC, abstractmethod

class WorkflowBase(ABC):
    def __init__(self, orchestrator):
        """
        Initializes the WorkflowBase class.

        Args:
            orchestrator (Orchestrator): An instance of the Orchestrator agent responsible for managing the workflow.
        """
        self.orchestrator = orchestrator
        self.agents = []
        self.tasks = []
        self.workflow = {}

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

    def add_agent(self, agent):
        """
        Adds an agent to the workflow.

        Args:
            agent (BaseAgent): An instance of an agent to be added to the workflow.
        """
        self.agents.append(agent)

    def add_task(self, task):
        """
        Adds a task to the workflow.

        Args:
            task (str): A description of the task to be added to the workflow.
        """
        self.tasks.append(task)

    def set_workflow(self, workflow):
        """
        Sets the workflow for the process.

        Args:
            workflow (dict): A dictionary representing the workflow, including agent-task interactions and execution sequence.
        """
        self.workflow = workflow

    def execute(self):
        """
        Executes the workflow using the Orchestrator. Defines the main logic for executing the workflow.
        """
        if not self.workflow:
            raise ValueError("Workflow is not defined.")
        self.orchestrator.execute(self.workflow)

    def __repr__(self):
        return f"<WorkflowBase agents={self.agents}, tasks={self.tasks}, workflow={self.workflow}>"
    
# Explanation:
# Initialization: Initializes with an Orchestrator instance, which will handle the execution of the workflow.

# Abstract Methods:

# define_agents(): To be implemented by subclasses to specify the agents involved in the workflow.
# define_tasks(): To be implemented by subclasses to specify the tasks.
# define_workflow(): To be implemented by subclasses to define the specific workflow, including how agents and tasks interact.
# Instance Methods:

# add_agent(agent): Adds an agent to the workflow.
# add_task(task): Adds a task to the workflow.
# set_workflow(workflow): Sets the workflow, detailing agent-task interactions and execution order.
# execute(): Uses the Orchestrator to run the defined workflow. Raises an error if the workflow is not defined.
# Representation: The __repr__ method provides a string representation of the WorkflowBase instance, showing its agents, tasks, and workflow.

# You would create subclasses of WorkflowBase to define specific workflows for different processes. Each subclass would implement the define_agents(), define_tasks(), and define_workflow() methods to detail how the workflow should be structured and executed.
