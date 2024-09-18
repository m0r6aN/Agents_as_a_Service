# agents/core_agents/notification_agent_main.py

import logging
from agents.core_agents.notification_agent import NotificationAgent

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')

def main():
    setup_logging()
    notification_agent = NotificationAgent()
    # The agent will start listening for messages upon initialization
    logging.getLogger('Main').info("NotificationAgent is running.")
    try:
        # Keep the script running
        while True:
            pass
    except KeyboardInterrupt:
        logging.getLogger('Main').info("NotificationAgent stopped.")

if __name__ == '__main__':
    main()
