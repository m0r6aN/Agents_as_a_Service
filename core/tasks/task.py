class Task:
    def __init__(self, description, agents):
        self.description = description
        self.agents = agents
        self.status = "Pending"

    def assign(self):
        for agent in self.agents:
            agent.execute()

    def update_status(self, status):
        self.status = status
