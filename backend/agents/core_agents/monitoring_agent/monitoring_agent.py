# agents/core_agents/monitoring_agent.py

import psutil
import logging
from time import sleep
from agents.agent_base import Agent

class MonitoringAgent(Agent):
    def __init__(self, check_interval=5):
        super().__init__(
            agent_name="MonitoringAgent",
            system_message="Monitor system resources and performance.",
            model_name="SLM-Monitoring",
            tools=None,
            config={'superior_agent_id': None}
        )
        self.logger = logging.getLogger(self.agent_name)
        self.check_interval = check_interval
        self.running = True

    def start_monitoring(self):
        self.logger.info("Starting system monitoring.")
        while self.running:
            self.check_system_resources()
            sleep(self.check_interval)

    def check_system_resources(self):
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        resource_status = {
            'cpu_usage': cpu_usage,
            'memory_available': memory_info.available,
            'memory_total': memory_info.total,
            'disk_free': disk_usage.free,
            'disk_total': disk_usage.total
        }
        self.logger.debug(f"Resource status: {resource_status}")
        self.evaluate_resources(resource_status)

    def evaluate_resources(self, resource_status):
        # Implement thresholds and alerts
        alerts = []
        if resource_status['cpu_usage'] > 80:
            alerts.append(f"High CPU usage detected: {resource_status['cpu_usage']}%")
        if resource_status['memory_available'] < 0.2 * resource_status['memory_total']:
            alerts.append("Low available memory detected.")
        if resource_status['disk_free'] < 0.1 * resource_status['disk_total']:
            alerts.append("Low disk space detected.")
        if alerts:
            alert_message = '\n'.join(alerts)
            self.logger.warning(alert_message)
            self.send_alert(alert_message)

    def send_alert(self, alert_message):
        # Send alert to NotificationAgent
        notification = {
            'subject': 'System Resource Alert',
            'message': alert_message,
            'recipients': ['admin@example.com']
        }
        self.communicate(str(notification), 'NotificationAgent')
        self.logger.debug("Alert sent to NotificationAgent.")

    def perform_task(self, task):
        # Not used in this agent
        pass
