# agents/core_agents/prompt_agent.py

import logging
from agents.agent_base import Agent

class PromptAgent(Agent):
    def __init__(self):
        super().__init__(
            agent_name="PromptAgent",
            system_message="Generate system prompts for agents based on tasks.",
            model_name="GPT-3.5",
            tools=None
        )
        self.logger = logging.getLogger(self.agent_name)

    def generate_prompt(self, task):
        prompt = f"""
You are assigned the task: {task.task_description}
Use the following tools: {', '.join(task.tools)}
Communicate effectively with superiors and subordinates.
Regularly report back and ask for permission when needed.
Consider delegating subtasks when appropriate.
"""
        self.logger.debug(f"Prompt generated for task {task.task_id}")
        return prompt
