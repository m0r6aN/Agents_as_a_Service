# agents/core_agents/security_agent_main.py

import logging
from agents.core_agents.security_agent import SecurityAgent

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')

def main():
    setup_logging()
    security_agent = SecurityAgent()
    security_agent.start_security_checks()

if __name__ == '__main__':
    main()
