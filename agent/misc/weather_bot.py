import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key)

assistant = client.beta.assistants.create(
  instructions="You are a weather bot. Use the provided functions to answer questions.",
  model="gpt-4o-mini",
  tools=[
    {
      "type": "function",
      "function": {
        "name": "get_latest_ohlcv",
        "description": "Gets the latest OHLCV (Open, High, Low, Close, Volume) data for a specific cryptocurrency",
        "parameters": {
          "type": "object",
          "properties": {
            "stmbol": {
              "type": "string",
              "description": "The symbol of the cryptocurrency, e.g., BTC, ETH, ADA"
            },
            "timeframe": {
              "type": "string",
              "description": "The temperature unit to use. Infer this from the user's location."
            }
          },
          "required": ["location", "unit"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "get_rain_probability",
        "description": "Get the probability of rain for a specific location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g., San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }
    }
  ]
)