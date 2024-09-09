class ExecutionContext:
    def __init__(self):
        self.state = {}
        self.completed_tasks = []

    def update_state(self, task, result):
        self.state[task] = result
        self.completed_tasks.append(task)

    def get_state(self):
        return self.state
