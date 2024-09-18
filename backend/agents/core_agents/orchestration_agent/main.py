# main.py

import logging
from agents.orchestrator.orchestrator import OrchestratorAgent
from messaging.messaging import MessagingClient

def setup_logging():
    """
    Sets up logging configuration for the application.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def main():
    """
    Main function to initialize the Orchestrator Agent and start listening for process requests.
    """
    setup_logging()
    logger = logging.getLogger('Main')
    logger.info("Starting the Orchestrator Agent.")

    # Initialize the Orchestrator Agent
    orchestrator = OrchestratorAgent()

    # Initialize the Messaging Client
    messaging_client = MessagingClient()

    # Define a callback function for incoming messages
    def on_message(ch, method, properties, body):
        message = body.decode()
        logger.debug(f"Received message: {message}")
        orchestrator.receive_message(message)

    # Start listening to the 'process_requests' queue
    logger.info("Orchestrator is now listening for process requests.")
    try:
        messaging_client.receive_messages('process_requests', on_message)
    except KeyboardInterrupt:
        logger.info("Orchestrator Agent has been stopped.")

if __name__ == '__main__':
    main()
