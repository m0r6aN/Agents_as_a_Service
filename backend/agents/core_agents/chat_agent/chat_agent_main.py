# agents/core_agents/chat_agent_main.py

import logging
from agents.core_agents.chat_agent import ChatAgent

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')

def main():
    setup_logging()
    chat_agent = ChatAgent()
    # The agent will start listening for messages upon initialization
    logging.getLogger('Main').info("ChatAgent is running.")
    try:
        # Keep the script running
        while True:
            pass
    except KeyboardInterrupt:
        logging.getLogger('Main').info("ChatAgent stopped.")

if __name__ == '__main__':
    main()
