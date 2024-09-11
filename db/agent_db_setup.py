# agents_as_a_service/db/agent_db_setup.py

import sqlite3

# Database initialization
def initialize_db(conn, close_conn=True):
    cursor = conn.cursor()

    # Create Agents table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Agents (
        agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT NOT NULL,
        agent_type TEXT NOT NULL,
        tools TEXT,  -- Storing tools as a comma-separated string for now, can switch to JSON if needed
        memory TEXT, -- Memory stored as JSON for flexibility
        state TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id INTEGER,
        task_name TEXT NOT NULL,
        task_status TEXT NOT NULL,
        result TEXT,  -- Store task result as text or JSON
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (agent_id) REFERENCES Agents(agent_id) ON DELETE CASCADE
    )
    ''')

    # Create AgentMemory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AgentMemory (
        memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id INTEGER,
        memory_data TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (agent_id) REFERENCES Agents(agent_id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    
    if close_conn:
        conn.close()
    
    print("Database initialized successfully!")

if __name__ == '__main__':
    initialize_db()
