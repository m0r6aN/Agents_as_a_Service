# agents/task.py

class Task:
    def __init__(self, task_id, task_name, task_description, capabilities, function,
                 dependencies=None, tools=None, retry_count=3, timeout=300, context=None,
                 status='PENDING', version='1.0'):
        self.task_id = task_id
        self.task_name = task_name
        self.task_description = task_description
        self.capabilities = capabilities
        self.function = function
        self.dependencies = dependencies if dependencies else []
        self.tools = tools if tools else []
        self.retry_count = retry_count
        self.timeout = timeout
        self.context = context if context else {}
        self.status = status
        self.version = version
