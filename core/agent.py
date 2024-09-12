import logging
from core.utils.db_interactions import DatabaseClient

class Agent:
    def __init__(self, agent_id, agent_name, tools=None, memory=None, config=None):
        """
        Initialize the agent with its name, tools, and other configurations.
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.tools = tools if tools else []
        self.memory = memory if memory else {}
        self.config = config if config else {}

        # Initialize database client for persistence
        self.db = DatabaseClient()

    def load_agent(self, agent_id):
        """
        Load agent configuration from the database.
        """
        agent_data = self.db.load_agent(agent_id)
        self.agent_name = agent_data['name']
        self.tools = agent_data['tools']
        self.memory = agent_data['memory']
        self.config = agent_data['config']

        logging.info(f"Loaded agent {self.agent_name} from database.")

    def save_agent(self):
        """
        Save the current state of the agent to the database.
        """
        agent_data = {
            'name': self.agent_name,
            'tools': self.tools,
            'memory': self.memory,
            'config': self.config
        }
        self.db.save_agent(agent_data)

        logging.info(f"Agent {self.agent_name} has been saved to the database.")

    async def execute_task(self, action, input_data):
        """
        Execute a task based on the provided action and input data.
        """
        logging.info(f"Agent {self.agent_name} is executing task {action}...")
        
        # Use the tools to process the action if applicable
        result = None
        if action in self.tools:
            result = await self.tools[action](input_data)
        else:
            logging.error(f"Agent {self.agent_name} does not have the tool to perform {action}.")
        
        # Store the result in the agent's memory
        self.memory[action] = result
        self.save_agent()  # Persist agent state after execution
        
        logging.info(f"Task {action} completed by {self.agent_name} with result: {result}")
        return result
