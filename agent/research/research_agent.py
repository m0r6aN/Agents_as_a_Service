from agents.base_agent import BaseAgent
from tools.google_search import GoogleSearchTool

class ResearchAgent(BaseAgent):
    def __init__(self, known_actions, default_prompt, system_message="", max_turns=5):
        super().__init__(known_actions, default_prompt, system_message, max_turns)
        self.tools = {
            "google_search": GoogleSearchTool()
        }

    def execute(self):
        # Example execution logic using a tool
        search_query = "latest advancements in quantum computing"
        result = self.tools["google_search"].use(search_query)
        self.add_message("system", result)

    def query(self, question):
        # Implement querying logic
        return f"ResearchAgent querying: {question}"

# Example usage
if __name__ == "__main__":
    known_actions = {}  # Define your known actions here
    agent = ResearchAgent(known_actions, "Default prompt", "System message", 5)
    agent.execute()
    for message in agent.messages:
        print(message)
