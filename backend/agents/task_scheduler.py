# agents/task_scheduler/task_scheduler.py

import threading
import json
import logging
from messaging.messaging import MessagingClient
from agents.task import Task

class TaskScheduler:
    def __init__(self):
        self.logger = logging.getLogger('TaskScheduler')
        self.messaging_client = MessagingClient()
        self.tasks = {}  # Stores tasks by task_id
        self.processes = {}  # Stores tasks grouped by process_id
        self.lock = threading.Lock()
        # Start listening for tasks
        threading.Thread(target=self.listen_for_tasks).start()

    def listen_for_tasks(self):
        self.messaging_client.receive_messages('task_scheduler', self.on_task_message)

    def on_task_message(self, ch, method, properties, body):
        message = json.loads(body.decode())
        process_id = message['process_id']
        task_data = message['task']
        task = Task(**task_data)
        with self.lock:
            self.tasks[task.task_id] = task
            if process_id not in self.processes:
                self.processes[process_id] = []
            self.processes[process_id].append(task)
        self.logger.debug(f"Received task {task.task_id} for process {process_id}.")
        self.schedule_tasks(process_id)

    def schedule_tasks(self, process_id):
        with self.lock:
            tasks = self.processes.get(process_id, [])
            for task in tasks:
                if task.status == 'PENDING' and self.dependencies_satisfied(task):
                    self.execute_task(task)

    def dependencies_satisfied(self, task):
        return all(self.tasks[dep_id].status == 'COMPLETED' for dep_id in task.dependencies)

    def execute_task(self, task):
        # Update task status
        task.status = 'IN_PROGRESS'
        self.logger.info(f"Executing task {task.task_id}.")
        # Send task to the appropriate agent's queue
        agent_queue = self.get_agent_queue(task.capabilities)
        if agent_queue:
            task_message = json.dumps(task.__dict__)
            self.messaging_client.send_message(agent_queue, task_message)
        else:
            self.logger.error(f"No agent available for capabilities: {task.capabilities}")
            task.status = 'FAILED'
            self.report_failure(task, "No agent available.")

    def get_agent_queue(self, capabilities):
        # Logic to find the agent queue based on capabilities
        # For simplicity, we'll assume a mapping
        capability_queue_map = {
            'nlp_to_sql': 'QueryAgentQueue',
            'database_operations': 'SQLAgentQueue',
            'template_management': 'TemplateAgentQueue',
            'report_generation': 'ReportAgentQueue'
        }
        return capability_queue_map.get(capabilities)

    def report_failure(self, task, error_message):
        # Update task status
        task.status = 'FAILED'
        # Report failure back to OrchestratorAgent or ChatAgent
        failure_message = {
            'task_id': task.task_id,
            'error': error_message
        }
        self.messaging_client.send_message('orchestrator_failures', json.dumps(failure_message))
        self.logger.debug(f"Reported failure for task {task.task_id}: {error_message}")

    # Additional methods to handle task completion, retries, etc.
