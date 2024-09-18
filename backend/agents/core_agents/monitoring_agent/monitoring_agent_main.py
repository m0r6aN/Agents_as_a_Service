# agents/core_agents/monitoring_agent_main.py

import logging
from agents.core_agents.monitoring_agent import MonitoringAgent

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')

def main():
    setup_logging()
    monitoring_agent = MonitoringAgent()
    monitoring_agent.start_monitoring()

if __name__ == '__main__':
    main()
