import threading
import json
import logging
from typing import Any, Dict, List
from messaging.messaging import MessagingClient
from agents.task import Task, TaskStatus

class TaskScheduler:
    def __init__(self):
        self.logger = logging.getLogger('TaskScheduler')
        self.messaging_client = MessagingClient()
        self.tasks: Dict[str, Task] = {}  # Stores tasks by task_id
        self.processes: Dict[str, List[Task]] = {}  # Stores tasks grouped by process_id
        self.lock = threading.Lock()
        self.max_parallel_tasks = 5  # Configurable parameter for parallel execution
        # Start listening for tasks
        threading.Thread(target=self.listen_for_tasks, daemon=True).start()

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
            executable_tasks = [
                task for task in tasks 
                if task.status == TaskStatus.PENDING and self.dependencies_satisfied(task)
            ]
            
            # Execute tasks in parallel up to max_parallel_tasks
            for task in executable_tasks[:self.max_parallel_tasks]:
                threading.Thread(target=self.execute_task, args=(task,), daemon=True).start()

    def dependencies_satisfied(self, task: Task) -> bool:
        return all(self.tasks[dep_id].status == TaskStatus.COMPLETED for dep_id in task.dependencies)

    def execute_task(self, task: Task):
        task.update_status(TaskStatus.IN_PROGRESS)
        self.logger.info(f"Executing task {task.task_id}.")
        agent_queue = self.get_agent_queue(task.capabilities)
        if agent_queue:
            task_message = json.dumps(task.__dict__)
            self.messaging_client.send_message(agent_queue, task_message)
        else:
            self.logger.error(f"No agent available for capabilities: {task.capabilities}")
            task.update_status(TaskStatus.FAILED)
            self.report_failure(task, "No agent available.")

    def get_agent_queue(self, capabilities: List[str]) -> str:
        # Logic to find the agent queue based on capabilities
        capability_queue_map = {
            'nlp_to_sql': 'QueryAgentQueue',
            'database_operations': 'SQLAgentQueue',
            'template_management': 'TemplateAgentQueue',
            'report_generation': 'ReportAgentQueue'
        }
        for capability in capabilities:
            if capability in capability_queue_map:
                return capability_queue_map[capability]
        return None

    def report_failure(self, task: Task, error_message: str):
        task.update_status(TaskStatus.FAILED)
        failure_message = {
            'task_id': task.task_id,
            'error': error_message
        }
        self.messaging_client.send_message('orchestrator_failures', json.dumps(failure_message))
        self.logger.debug(f"Reported failure for task {task.task_id}: {error_message}")

    def on_task_completion(self, task_id: str, result: Any):
        with self.lock:
            task = self.tasks.get(task_id)
            if task:
                task.update_status(TaskStatus.COMPLETED)
                self.logger.info(f"Task {task_id} completed successfully.")
                # Reschedule tasks that might now be ready
                for process_id, tasks in self.processes.items():
                    if task in tasks:
                        self.schedule_tasks(process_id)
                        break

    def retry_failed_tasks(self):
        with self.lock:
            for task in self.tasks.values():
                if task.status == TaskStatus.FAILED and task.retry_count > 0:
                    task.retry_count -= 1
                    task.update_status(TaskStatus.PENDING)
                    self.logger.info(f"Retrying task {task.task_id}. Attempts left: {task.retry_count}")
                    self.schedule_tasks(task.process_id)