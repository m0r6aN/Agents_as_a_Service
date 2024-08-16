from agents.base_agent import BaseAgent

class PromptAgent(BaseAgent):
    def modify_with_prompt(self, prompt):
        # Modify agent based on the given prompt
        self.add_message("system", prompt)