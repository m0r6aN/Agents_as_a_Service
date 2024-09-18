# agents/core_agents/chat_agent.py

import json
import logging
import uuid
from agents.agent_base import Agent
from agents.process_request import ProcessRequest
from agents.task import Task
from messaging.messaging import MessagingClient

class ChatAgent(Agent):
    def __init__(self):
        super().__init__(
            agent_name="ChatAgent",
            system_message="Assist users via chat interface for searching, reporting, and help.",
            model_name="GPT-3.5",
            tools=None,
            config={'superior_agent_id': None}
        )
        self.logger = logging.getLogger(self.agent_name)
        self.messaging_client = MessagingClient()
        # Start listening for chat messages
        self.messaging_client.receive_messages('ChatAgent', self.on_chat_message)

    def on_chat_message(self, ch, method, properties, body):
        message = body.decode()
        self.logger.debug(f"Received chat message: {message}")
        response = self.process_message(message)
        # Send response back to user
        user_id = properties.headers.get('user_id', 'unknown_user')
        self.send_response(user_id, response)

    def process_message(self, message):
        if self.is_query_request(message):
            # Generate a unique process ID
            process_id = f"process_{uuid.uuid4()}"

            # Define Tasks
            tasks = [
                Task(
                    task_id="task_convert_sql",
                    task_name="ConvertToSQL",
                    task_description="Convert natural language to SQL query.",
                    capabilities="nlp_to_sql",
                    function="convert_to_sql",
                    dependencies=[],
                    context={"user_message": message, "user_id": self.user_id}
                ),
                Task(
                    task_id="task_execute_sql",
                    task_name="ExecuteSQLQuery",
                    task_description="Execute SQL query to fetch report data.",
                    capabilities="database_operations",
                    function="execute_sql_query",
                    dependencies=["task_convert_sql"],
                    context={"user_id": self.user_id}
                ),
                Task(
                    task_id="task_get_template",
                    task_name="GetReportTemplate",
                    task_description="Retrieve report template.",
                    capabilities="template_management",
                    function="get_report_template",
                    dependencies=[],
                    context={"template_name": "default_report", "user_id": self.user_id}
                ),
                Task(
                    task_id="task_build_report",
                    task_name="BuildReport",
                    task_description="Build report using data and template.",
                    capabilities="report_generation",
                    function="build_report",
                    dependencies=["task_execute_sql", "task_get_template"],
                    context={"user_id": self.user_id}
                )
            ]

            # Create ProcessRequest
            process_request = ProcessRequest(process_id=process_id, tasks=tasks)

            # Send ProcessRequest to OrchestratorAgent
            message = json.dumps(process_request, default=lambda o: o.__dict__)
            self.messaging_client.send_message('process_requests', message)
            response = "Your report request is being processed. You will receive it shortly."
        else:
                response = f"You said: {message}"
        return response

    def send_response(self, user_id, response):
        # Placeholder for sending response back to user
        self.messaging_client.send_message(f'user_{user_id}', response)
        self.logger.debug(f"Response sent to user {user_id}: {response}")

    def perform_task(self, task):
        # Not used in this agent
        pass
