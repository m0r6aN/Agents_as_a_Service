import json
import sqlite3

class DatabaseClient:
    def __init__(self, conn=None):
        self.conn = conn or sqlite3.connect('agents_db.sqlite')

    def connect(self):
        return self.conn  # Always return the same connection

    # AGENT OPERATIONS
    def save_agent(self, agent_data):
        """
        Save or update agent information in the database.
        """
        conn = self.connect()
        cursor = conn.cursor()

        if 'agent_id' in agent_data and self.agent_exists(agent_data['agent_id']):
            # Update existing agent
            cursor.execute('''
            UPDATE Agents
            SET agent_name = ?, agent_type = ?, tools = ?, memory = ?, state = ?, last_updated = CURRENT_TIMESTAMP
            WHERE agent_id = ?
            ''', (agent_data['name'], agent_data['type'], 
                ','.join(agent_data['tools']), json.dumps(agent_data['memory']), 
                agent_data['state'], agent_data['agent_id']))
        else:
            # Insert new agent
            cursor.execute('''
            INSERT INTO Agents (agent_name, agent_type, tools, memory, state)
            VALUES (?, ?, ?, ?, ?)
            ''', (agent_data['name'], agent_data['type'], 
                ','.join(agent_data['tools']), json.dumps(agent_data['memory']), 
                agent_data['state']))

        conn.commit()

    def load_agent(self, agent_id):
        """
        Load agent information from the database.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Agents WHERE agent_id = ?', (agent_id,))
        agent_row = cursor.fetchone()

        if agent_row:
            return {
                'agent_id': agent_row[0],
                'name': agent_row[1],
                'type': agent_row[2],
                'tools': agent_row[3].split(','),
                'memory': json.loads(agent_row[4]),
                'state': agent_row[5],
                'created_at': agent_row[6],
                'last_updated': agent_row[7]
            }
        return None

    def agent_exists(self, agent_id):
        """
        Check if an agent exists in the database.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(1) FROM Agents WHERE agent_id = ?', (agent_id,))
        exists = cursor.fetchone()[0] > 0
        return exists

    # TASK OPERATIONS
    def save_task(self, task_data):
        """
        Save task result for a specific agent.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO Tasks (agent_id, task_name, task_status, result)
        VALUES (?, ?, ?, ?)
        ''', (task_data['agent_id'], task_data['task_name'], task_data['task_status'], task_data['result']))

        conn.commit()

    def load_tasks_by_agent(self, agent_id):
        """
        Load all tasks for a given agent.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Tasks WHERE agent_id = ?', (agent_id,))
        tasks = cursor.fetchall()

        return [{
            'task_id': task[0],
            'agent_id': task[1],
            'task_name': task[2],
            'task_status': task[3],
            'result': task[4],
            'created_at': task[5]
        } for task in tasks]
        
    def get_agent_config_for_task(self, task_name):
        # Query the database for the agent configuration based on the task
        query = "SELECT * FROM agent_configs WHERE task_name = ?"
        result = self.execute_query(query, [task_name])
        
        if result:
            return result[0]  # Return the config details
        return None

    def relate_agent_to_config(self, agent_id, config_id):
        # Insert relationship between agent and config into the database
        query = "INSERT INTO agent_config_relationships (agent_id, config_id) VALUES (?, ?)"
        self.execute_query(query, [agent_id, config_id])


    # AGENT MEMORY OPERATIONS
    def save_memory(self, agent_id, memory_data):
        """
        Save memory for a given agent.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO AgentMemory (agent_id, memory_data)
        VALUES (?, ?)
        ''', (agent_id, json.dumps(memory_data)))

        conn.commit()

    def load_memory(self, agent_id):
        """
        Load memory data for a specific agent.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT memory_data FROM AgentMemory WHERE agent_id = ?', (agent_id,))
        memories = cursor.fetchall()

        return [json.loads(memory[0]) for memory in memories]
