import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key)

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  tool_choice="auto",
  parallel_tool_calls="",
)

print(completion.choices[0].message)

# https://platform.openai.com/docs/api-reference/chat/create?lang=python
