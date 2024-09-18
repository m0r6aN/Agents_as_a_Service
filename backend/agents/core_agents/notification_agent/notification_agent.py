# agents/core_agents/notification_agent.py

import logging
import json
from agents.agent_base import Agent
from messaging.messaging import MessagingClient

class NotificationAgent(Agent):
    def __init__(self):
        super().__init__(
            agent_name="NotificationAgent",
            system_message="Send notifications to users or other agents.",
            model_name="SLM-Notification",
            tools=None,
            config={'superior_agent_id': None}
        )
        self.logger = logging.getLogger(self.agent_name)
        self.messaging_client = MessagingClient()
        # Start listening for notifications
        self.messaging_client.receive_messages('NotificationAgent', self.on_notification_message)

    def on_notification_message(self, ch, method, properties, body):
        notification = body.decode()
        self.logger.debug(f"Received notification: {notification}")
        self.process_notification(notification)

    def process_notification(self, notification):
        # Assuming notification is a JSON string
        notification_data = json.loads(notification)
        subject = notification_data.get('subject')
        message = notification_data.get('message')
        recipients = notification_data.get('recipients', [])
        for recipient in recipients:
            self.send_email(recipient, subject, message)
            self.logger.info(f"Notification sent to {recipient}")

    def send_email(self, recipient, subject, message):
        # Placeholder for email sending logic
        self.logger.debug(f"Sending email to {recipient} with subject '{subject}' and message '{message}'")

    def perform_task(self, task):
        # Not used in this agent
        pass
