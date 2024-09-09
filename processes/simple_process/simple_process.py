from core.process_base import ProcessBase, ExecutionContext
from agent.orchestrator import Orchestrator

class SimpleProcess(ProcessBase):
    def __init__(self, orchestrator: Orchestrator):
        super().__init__(orchestrator)
        self.define_agents()
        self.define_tasks()
        self.define_workflow()

    def define_agents(self):
        # Assuming we're only using the orchestrator for this simple example
        self.add_agent(self.orchestrator)

    def define_tasks(self):
        # Define simple tasks with descriptions
        self.add_task("Task 1", dependencies=[])
        self.add_task("Task 2", dependencies=["Task 1"])
        self.add_task("Task 3", dependencies=["Task 1", "Task 2"])

    def define_workflow(self):
        # Set up the workflow based on the defined tasks
        workflow = {
            "Task 1": {"agent": "Orchestrator", "dependencies": []},
            "Task 2": {"agent": "Orchestrator", "dependencies": ["Task 1"]},
            "Task 3": {"agent": "Orchestrator", "dependencies": ["Task 1", "Task 2"]}
        }
        self.set_workflow(workflow)
