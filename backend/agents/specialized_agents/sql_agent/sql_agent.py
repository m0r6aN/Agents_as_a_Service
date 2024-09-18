# agents/specialized_agents/sql_agent.py

import json
import logging
from agents.agent_base import Agent
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from messaging.messaging import MessagingClient
from datetime import datetime, timedelta

Base = declarative_base()

# Example ORM model
class ExampleModel(Base):
    __tablename__ = 'example_table'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class SQLAgent(Agent):
    def __init__(self, database_url, agent_name='SQLAgent', tools=None, memory=None, config=None):
        super().__init__(
            agent_name=agent_name,
            system_message="Perform database operations using ORM.",
            model_name="SQL-Model",
            tools=tools,
            memory=memory,
            config=config
        )
        self.logger = logging.getLogger(self.agent_name)
        self.database_url = database_url
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.messaging_client = MessagingClient()
    
    def perform_task(self, task):
        try:
            # Execute the task function
            result = self.execute_sql_query(task.context)
            task.status = 'COMPLETED'
            self.logger.info(f"Task {task.task_id} completed successfully.")
            # Report completion to TaskScheduler
            self.report_task_completion(task)
        except Exception as e:
            task.status = 'FAILED'
            self.logger.error(f"Task {task.task_id} failed: {str(e)}")
            self.report_failure(e)

    def report_task_completion(self, task):
        message = {
            'task_id': task.task_id,
            'status': task.status,
            'result': task.context.get('result')
        }
        self.messaging_client.send_message('task_scheduler', json.dumps(message))
        self.logger.debug(f"Reported completion of task {task.task_id} to TaskScheduler.")
    
    def create_record(self, context):
        """
        Creates a new record in the database.
        """
        session = self.Session()
        try:
            name = context.get('name')
            description = context.get('description')

            # Input validation
            if not isinstance(name, str) or not isinstance(description, str):
                raise ValueError("Invalid input types for name or description.")

            # Create a new record using ORM
            new_record = ExampleModel(
                name=name,
                description=description
            )
            session.add(new_record)
            session.commit()
            self.logger.debug(f"Record created with ID: {new_record.id}")
            return {'status': 'success', 'id': new_record.id}
        except (SQLAlchemyError, ValueError) as e:
            session.rollback()
            self.logger.error(f"Error creating record: {e}")
            raise
        finally:
            session.close()
    
    def read_records(self, context):
        """
        Reads records from the database based on filters.
        """
        session = self.Session()
        try:
            query = session.query(ExampleModel)
            filters = context.get('filters', {})
            for attr, value in filters.items():
                query = query.filter(getattr(ExampleModel, attr) == value)
            records = query.all()
            result = [{'id': record.id, 'name': record.name, 'description': record.description} for record in records]
            self.logger.debug(f"Read {len(records)} records.")
            return {'status': 'success', 'records': result}
        except SQLAlchemyError as e:
            self.logger.error(f"Error reading records: {e}")
            raise
        finally:
            session.close()
    
    def update_record(self, context):
        """
        Updates a record in the database.
        """
        session = self.Session()
        try:
            record_id = context.get('id')
            updates = context.get('updates', {})
            record = session.query(ExampleModel).get(record_id)
            if not record:
                raise ValueError(f"Record with ID {record_id} not found.")
            for attr, value in updates.items():
                setattr(record, attr, value)
            session.commit()
            self.logger.debug(f"Record with ID {record_id} updated.")
            return {'status': 'success', 'id': record_id}
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error updating record: {e}")
            raise
        finally:
            session.close()
    
    def delete_record(self, context):
        """
        Deletes a record from the database.
        """
        session = self.Session()
        try:
            record_id = context.get('id')
            record = session.query(ExampleModel).get(record_id)
            if not record:
                raise ValueError(f"Record with ID {record_id} not found.")
            session.delete(record)
            session.commit()
            self.logger.debug(f"Record with ID {record_id} deleted.")
            return {'status': 'success', 'id': record_id}
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error deleting record: {e}")
            raise
        finally:
            session.close()
    
    def advanced_query(self, context):
        """
        Performs an advanced query using ORM.
        """
        session = self.Session()
        try:
            # Only allow specific, parameterized queries
            query_type = context.get('query_type')
            if query_type == 'recent_records':
                days = context.get('days', 7)
                if not isinstance(days, int):
                    raise ValueError("Invalid input type for days.")

                query = session.query(ExampleModel).filter(
                    ExampleModel.created_at >= datetime.utcnow() - timedelta(days=days)
                )
            else:
                raise ValueError("Unsupported query type.")

            records = query.all()
            result = [{'id': record.id, 'name': record.name, 'description': record.description} for record in records]
            self.logger.debug(f"Advanced query returned {len(records)} records.")
            return {'status': 'success', 'records': result}
        except (SQLAlchemyError, ValueError) as e:
            self.logger.error(f"Error in advanced query: {e}")
            raise
        finally:
            session.close()
