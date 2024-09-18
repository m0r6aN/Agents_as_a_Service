# main.py

import logging
import logging.config
from config.settings import LOGGING_CONFIG_FILE
from agents.orchestrator.orchestrator import OrchestratorAgent
from messaging.messaging import MessagingClient

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')

def main():
    setup_logging()
    logger = logging.getLogger('Main')
    orchestrator = OrchestratorAgent()
    messaging_client = MessagingClient()

    def on_message(ch, method, properties, body):
        orchestrator.receive_message(body.decode())

    logger.info("Orchestrator is starting to listen for process requests.")
    messaging_client.receive_messages('process_requests', on_message)

if __name__ == '__main__':
    main()
