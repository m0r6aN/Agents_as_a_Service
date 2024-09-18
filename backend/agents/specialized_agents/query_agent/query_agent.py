# agents/specialized_agents/query_agent.py

import logging
import openai
from agents.agent_base import Agent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from agents.specialized_agents.sql_agent import Base, ExampleModel
from datetime import datetime, timedelta

class QueryAgent(Agent):
    def __init__(self):
        super().__init__(
            agent_name="QueryAgent",
            system_message="Convert natural language queries into ORM queries and execute them.",
            model_name="GPT-3.5",
            tools=None,
            config={'superior_agent_id': None}
        )
        self.logger = logging.getLogger(self.agent_name)
        # Database setup
        self.database_url = 'sqlite:///query_agent.db'
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def perform_task(self, task):
        self.logger.info(f"Starting task {task.task_id}: {task.task_name}")
        try:
            message = task.context.get('message')
            user_id = task.context.get('user_id', 'unknown_user')
            # Parse and execute the query
            results = self.handle_natural_language_query(message)
            # Format results
            response = self.format_results(results)
            # Send response back to ChatAgent or user
            self.report_to_superior({'user_id': user_id, 'response': response})
        except Exception as e:
            task.status = 'FAILED'
            self.logger.error(f"Task {task.task_id} failed: {str(e)}")
            self.report_failure(e)
    
    # To improve the accuracy of parsing natural language queries, integrate an NLP model or service.
    # Options:
    # Custom NLP Models: Train a custom model using libraries like spaCy or NLTK.
    # Pre-trained Models: Use pre-trained models like OpenAI's GPT-3 via API.
    # NLU Services: Utilize services like Microsoft LUIS, Google Dialogflow, or IBM Watson.
    def parse_query(self, message):
        # Set your OpenAI API key
        openai.api_key = 'YOUR_API_KEY'
        prompt = f"Extract query parameters from the following request:\n\n{message}\n\nParameters:"
        response = openai.Completion.create(
            engine='davinci',
            prompt=prompt,
            max_tokens=150,
            temperature=0.0
        )
        parameters_text = response.choices[0].text.strip()
        # Parse the parameters_text into a dictionary
        query_params = self.extract_parameters(parameters_text)
        self.logger.debug(f"Parsed query parameters: {query_params}")
        return query_params
    
    def format_results(self, results):
        # Format the query results into a user-friendly message
        if not results:
            return "No records found for your query."
        response_lines = ["Here are the results of your query:"]
        for record in results:
            line = f"Order ID: {record.id}, Customer: {record.name}, Date: {record.created_at.strftime('%Y-%m-%d')}"
            response_lines.append(line)
        return '\n'.join(response_lines)
    
    def report_to_superior(self, result):
        message = f"Query results for user {result['user_id']}: {result['response']}"
        self.communicate(message, self.config.get('superior_agent_id'))
        self.logger.debug(f"Reported to superior: {message}")
