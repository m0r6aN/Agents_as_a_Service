# utils/utils.py

import json
import logging
import uuid
from utils.constants import *

def generate_unique_id():
    """
    Generates a unique identifier using UUID4.
    """
    return str(uuid.uuid4())

def load_json_from_file(file_path):
    """
    Loads JSON data from a file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json_to_file(data, file_path):
    """
    Saves JSON data to a file.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def serialize_function(function):
    """
    Serializes a function to a string representation.
    """
    # Placeholder for function serialization logic
    return function.__name__

def deserialize_function(function_name):
    """
    Deserializes a function from a string representation.
    """
    # Placeholder for function deserialization logic
    # Needs access to the function's module and namespace
    return globals().get(function_name)

def setup_logging():
    """
    Sets up logging configuration.
    """
    logging.basicConfig(
        level=getattr(logging, LOGGING_LEVEL),
        format=LOGGING_FORMAT,
        handlers=[
            logging.StreamHandler()
        ]
    )

def validate_task_data(task_data):
    """
    Validates task data to ensure all required fields are present.
    """
    required_fields = [
        'task_id',
        'task_name',
        'task_description',
        'capabilities',
        'tools',
        'dependencies',
        'retry_count',
        'timeout',
        'context',
        'status',
        'version',
        'function'
    ]
    missing_fields = [field for field in required_fields if field not in task_data]
    if missing_fields:
        raise ValueError(f"Missing required task fields: {', '.join(missing_fields)}")
    return True

def validate_agent_data(agent_data):
    """
    Validates agent data to ensure all required fields are present.
    """
    required_fields = [
        'agent_id',
        'agent_name',
        'system_message',
        'model_name',
        'tools',
        'memory',
        'config'
    ]
    missing_fields = [field for field in required_fields if field not in agent_data]
    if missing_fields:
        raise ValueError(f"Missing required agent fields: {', '.join(missing_fields)}")
    return True

def parse_message(message):
    """
    Parses a JSON message and returns the corresponding data.
    """
    try:
        data = json.loads(message)
        return data
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON message: {e}")
        return None

def format_notification(subject, message, recipients):
    """
    Formats a notification message.
    """
    notification = {
        'subject': subject,
        'message': message,
        'recipients': recipients
    }
    return json.dumps(notification)

def get_agent_queue_name(agent_id):
    """
    Returns the messaging queue name for a given agent.
    """
    return f"agent_queue_{agent_id}"

def is_task_completed(task_status):
    """
    Checks if a task status indicates completion.
    """
    return task_status == TASK_STATUS_COMPLETED
