from agents.agent_base import Agent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from agents.specialized_agents.sql_agent import Base, ExampleModel
from datetime import datetime, timedelta
import openai
from typing import Any, Dict, List

class QueryAgent(Agent):
    def __init__(self, agent_name: str, system_message: str, model_name: str, tools: List[str] = None, memory: Dict[str, Any] = None, config: Dict[str, Any] = None):
        super().__init__(agent_name, system_message, model_name, tools, memory, config)
        
        # Database setup
        self.database_url = 'sqlite:///query_agent.db'
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def perform_task(self, task: Any) -> Any:
        self.logger.info(f"Starting task {task.task_id}: {task.task_name}")
        try:
            message = task.context.get('message')
            user_id = task.context.get('user_id', 'unknown_user')
            # Parse and execute the query
            results = self.handle_natural_language_query(message)
            # Format results
            response = self.format_results(results)
            # Send response back to ChatAgent or user
            self.report_completion(task.task_id, {'user_id': user_id, 'response': response})
            return response
        except Exception as e:
            self.logger.error(f"Task {task.task_id} failed: {str(e)}")
            self.report_failure(task.task_id, str(e))
            raise

    def parse_query(self, message: str) -> Dict[str, Any]:
        # Set your OpenAI API key
        openai.api_key = self.config.get('openai_api_key', 'YOUR_API_KEY')
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

    def handle_natural_language_query(self, message: str) -> Any:
        query_params = self.parse_query(message)
        # Use the query_params to construct and execute an ORM query
        # This is a placeholder and should be implemented based on your specific ORM and database schema
        session = self.Session()
        try:
            results = session.query(ExampleModel).filter_by(**query_params).all()
            return results
        finally:
            session.close()

    def format_results(self, results: List[Any]) -> str:
        if not results:
            return "No records found for your query."
        response_lines = ["Here are the results of your query:"]
        for record in results:
            line = f"Order ID: {record.id}, Customer: {record.name}, Date: {record.created_at.strftime('%Y-%m-%d')}"
            response_lines.append(line)
        return '\n'.join(response_lines)

    def extract_parameters(self, parameters_text: str) -> Dict[str, Any]:
        # This is a placeholder method. Implement the logic to parse the parameters_text into a dictionary.
        # For example, you might split the text by newlines and then by colons to get key-value pairs.
        params = {}
        for line in parameters_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                params[key.strip()] = value.strip()
        return params