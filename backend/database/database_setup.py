# database/database_setup.py

import sqlite3
import logging

class Database:
    def __init__(self, db_file='aaas.db'):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.create_tables()
        self.logger = logging.getLogger('Database')

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                agent_name TEXT,
                system_message TEXT,
                model_name TEXT,
                tools TEXT,
                memory TEXT,
                config TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tools (
                tool_id TEXT PRIMARY KEY,
                tool_name TEXT,
                tool_description TEXT,
                version TEXT,
                function TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                task_name TEXT,
                task_description TEXT,
                capabilities TEXT,
                tools TEXT,
                dependencies TEXT,
                retry_count INTEGER,
                timeout INTEGER,
                context TEXT,
                status TEXT,
                version TEXT,
                function TEXT
            )
        ''')
        self.conn.commit()
        self.logger.debug("Database tables created.")

    def save_agent(self, agent_data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO agents (agent_id, agent_name, system_message, model_name, tools, memory, config)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            agent_data['agent_id'],
            agent_data['agent_name'],
            agent_data['system_message'],
            agent_data['model_name'],
            ','.join(agent_data['tools']),
            str(agent_data['memory']),
            str(agent_data['config'])
        ))
        self.conn.commit()
        self.logger.debug(f"Agent {agent_data['agent_id']} saved to database.")

    def update_agent_tools(self, agent_id, tools):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE agents SET tools = ? WHERE agent_id = ?
        ''', (','.join(tools), agent_id))
        self.conn.commit()
        self.logger.debug(f"Agent {agent_id} tools updated.")

    def update_agent_memory(self, agent_id, memory):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE agents SET memory = ? WHERE agent_id = ?
        ''', (str(memory), agent_id))
        self.conn.commit()
        self.logger.debug(f"Agent {agent_id} memory updated.")

    def save_tool(self, tool_data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO tools (tool_id, tool_name, tool_description, version, function)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            tool_data['tool_id'],
            tool_data['tool_name'],
            tool_data['tool_description'],
            tool_data['version'],
            tool_data['function']  # Serialize function appropriately
        ))
        self.conn.commit()
        self.logger.debug(f"Tool {tool_data['tool_id']} saved to database.")

    def find_agent_by_capabilities(self, capabilities):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM agents WHERE agent_name LIKE ?
        ''', ('%' + capabilities + '%',))
        result = cursor.fetchone()
        if result:
            agent_data = {
                'agent_id': result[0],
                'agent_name': result[1],
                'system_message': result[2],
                'model_name': result[3],
                'tools': result[4].split(','),
                'memory': eval(result[5]),
                'config': eval(result[6])
            }
            self.logger.debug(f"Agent found with capabilities: {capabilities}")
            return agent_data
        else:
            self.logger.debug(f"No agent found with capabilities: {capabilities}")
            return None
