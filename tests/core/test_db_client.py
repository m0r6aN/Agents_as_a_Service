import sqlite3
import pytest
from core.utils.db_interactions import DatabaseClient
from db.agent_db_setup import initialize_db

@pytest.fixture
def db_client():
    # Use in-memory SQLite database for testing
    conn = sqlite3.connect(':memory:')
    
    # Initialize the database schema using the same connection
    initialize_db(conn, False)
    
    # Return the DatabaseClient instance with the same connection
    return DatabaseClient(conn)

def test_save_and_load_agent(db_client):
    agent_data = {
        'name': 'Agent_1',
        'type': 'Static',
        'tools': ['tool_1', 'tool_2'],
        'memory': {'task_1': 'result_1'},
        'state': 'idle'
    }

    # Save agent to the database
    db_client.save_agent(agent_data)

    # Load the agent back from the database
    saved_agent = db_client.load_agent(1)  # Assuming it gets the first ID
    
    assert saved_agent['name'] == 'Agent_1'
    assert saved_agent['type'] == 'Static'
    assert saved_agent['tools'] == ['tool_1', 'tool_2']
    assert saved_agent['memory'] == {'task_1': 'result_1'}
    assert saved_agent['state'] == 'idle'

def test_update_agent(db_client):
    agent_data = {
        'name': 'Agent_1',
        'type': 'Static',
        'tools': ['tool_1', 'tool_2'],
        'memory': {'task_1': 'result_1'},
        'state': 'idle'
    }

    # Save agent to the database
    db_client.save_agent(agent_data)

    # Retrieve the agent ID (assuming it's the first agent)
    saved_agent = db_client.load_agent(1)
    agent_id = saved_agent['agent_id']

    # Update the agent data with the agent ID
    updated_agent_data = {
        'agent_id': agent_id,  # Make sure the agent_id is included
        'name': 'Updated_Agent',
        'type': 'Static',
        'tools': ['tool_3'],
        'memory': {'task_2': 'result_2'},
        'state': 'active'
    }

    # Update the agent
    db_client.save_agent(updated_agent_data)

    # Load the updated agent
    updated_agent = db_client.load_agent(agent_id)
    
    assert updated_agent['name'] == 'Updated_Agent'
    assert updated_agent['tools'] == ['tool_3']
    assert updated_agent['memory'] == {'task_2': 'result_2'}
    assert updated_agent['state'] == 'active'


def test_save_and_load_task(db_client):
    # First, insert an agent to associate with the task
    agent_data = {
        'name': 'Agent_1',
        'type': 'Static',
        'tools': ['tool_1'],
        'memory': {},
        'state': 'idle'
    }
    db_client.save_agent(agent_data)

    # Save a task
    task_data = {
        'agent_id': 1,  # Assuming the first agent gets ID 1
        'task_name': 'task_1',
        'task_status': 'completed',
        'result': 'Task 1 result'
    }
    db_client.save_task(task_data)

    # Load tasks for the agent
    tasks = db_client.load_tasks_by_agent(1)
    assert len(tasks) == 1
    assert tasks[0]['task_name'] == 'task_1'
    assert tasks[0]['task_status'] == 'completed'
    assert tasks[0]['result'] == 'Task 1 result'

def test_save_and_load_memory(db_client):
    # First, insert an agent to associate with the memory
    agent_data = {
        'name': 'Agent_1',
        'type': 'Static',
        'tools': ['tool_1'],
        'memory': {},
        'state': 'idle'
    }
    db_client.save_agent(agent_data)

    # Save memory for the agent
    memory_data = {'task_1': 'result_1'}
    db_client.save_memory(1, memory_data)

    # Load memory for the agent
    memories = db_client.load_memory(1)
    assert len(memories) == 1
    assert memories[0] == {'task_1': 'result_1'}
