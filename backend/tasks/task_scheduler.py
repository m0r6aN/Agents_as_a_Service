# main.py
from core.agents.orchestration.orchestrator_agent import OrchestrationAgent

if __name__ == '__main__':
    # Initialize the Orchestration Agent
    orchestration_agent = OrchestrationAgent()
    # Perform the task
    orchestration_agent.perform_task()
