# chatbot.py

import re
import os
from openai import OpenAI
from ..base_agent import BaseAgent
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

class ChatBot(BaseAgent):
    def __init__(self, known_actions, default_prompt, system_message="", max_turns=5):
        super().__init__(known_actions, default_prompt, system_message, max_turns)
        self.action_re = re.compile('^Action: (\w+): (.*)$')
        self.client = OpenAI(api_key=openai_api_key)

    def execute(self):
        chat_completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return chat_completion.choices[0].message.content

    def query(self, question):
        i = 0
        next_prompt = self.default_prompt + "\n\nQuestion: " + question
        while i < self.max_turns:
            i += 1
            self.add_message("user", next_prompt)
            result = self.execute()
            self.add_message("assistant", result)
            print(result)
            actions = [self.action_re.match(a) for a in result.split('\n') if self.action_re.match(a)]
            if actions:
                action, action_input = actions[0].groups()
                print(f" -- running {action}: {action_input}")
                observation = self.run_action(action, action_input)
                print("Observation:", observation)
                next_prompt = f"Observation: {observation}"
            else:
                return result
        return "Max turns reached without a final answer."