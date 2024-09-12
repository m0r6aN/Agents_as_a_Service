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
    
    # Create AgentConfigs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AgentConfigs (
        agent_id TEXT PRIMARY KEY,  -- Unique identifier for the agent
    chat_model TEXT,
    utility_model TEXT,
    embeddings_model TEXT,
    prompts_subdir TEXT,
    memory_subdir TEXT,
    knowledge_subdir TEXT,
    auto_memory_count INTEGER DEFAULT 3,
    auto_memory_skip INTEGER DEFAULT 2,
    rate_limit_seconds INTEGER DEFAULT 60,
    rate_limit_requests INTEGER DEFAULT 15,
    rate_limit_input_tokens INTEGER DEFAULT 0,
    rate_limit_output_tokens INTEGER DEFAULT 0,
    msgs_keep_max INTEGER DEFAULT 25,
    msgs_keep_start INTEGER DEFAULT 5,
    msgs_keep_end INTEGER DEFAULT 10,
    response_timeout_seconds INTEGER DEFAULT 60,
    max_tool_response_length INTEGER DEFAULT 3000,
    code_exec_docker_enabled BOOLEAN DEFAULT 1,
    code_exec_docker_name TEXT,
    code_exec_docker_image TEXT,
    code_exec_docker_ports TEXT,  -- Store as JSON
    code_exec_docker_volumes TEXT, -- Store as JSON
    code_exec_ssh_enabled BOOLEAN DEFAULT 1,
    code_exec_ssh_addr TEXT,
    code_exec_ssh_port INTEGER DEFAULT 50022,
    code_exec_ssh_user TEXT,
    code_exec_ssh_pass TEXT,
    additional TEXT,  -- Store extra data as JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create AgentTasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AgentTasks (
        task_id TEXT PRIMARY KEY,  
        agent_id TEXT NOT NULL,    
        task_name TEXT NOT NULL,   
        task_description TEXT,     
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (agent_id) REFERENCES agent_configs(agent_id)
    )
    ''')
    
    # Create Tools table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tools (
        tool_id TEXT PRIMARY KEY,   
        tool_name TEXT NOT NULL,    
        tool_description TEXT       
    )
    ''')    
    
    # Create TaskTools table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TaskTools (
        task_id TEXT NOT NULL,      
        tool_id TEXT NOT NULL,      
        PRIMARY KEY (task_id, tool_id),
        FOREIGN KEY (task_id) REFERENCES agent_tasks(task_id),
        FOREIGN KEY (tool_id) REFERENCES tools(tool_id)   
    )
    ''')
    
    # Sample AgentConfigs data
    cursor.execute('''
        INSERT INTO agent_configs (
        agent_id, chat_model, utility_model, embeddings_model, prompts_subdir,
        memory_subdir, knowledge_subdir, auto_memory_count, auto_memory_skip,
        rate_limit_seconds, rate_limit_requests, rate_limit_input_tokens,
        rate_limit_output_tokens, msgs_keep_max, msgs_keep_start, msgs_keep_end,
        response_timeout_seconds, max_tool_response_length, code_exec_docker_enabled,
        code_exec_docker_name, code_exec_docker_image, code_exec_docker_ports,
        code_exec_docker_volumes, code_exec_ssh_enabled, code_exec_ssh_addr,
        code_exec_ssh_port, code_exec_ssh_user, code_exec_ssh_pass, additional
        ) VALUES (
        'agent_001', 'gpt-4', 'davinci-003', 'text-embedding-ada-002', 'prompts/web_search',
        'memory/web_search', 'knowledge/web_search', 3, 2, 60, 15, 1000, 500, 25, 5, 10,
        60, 3000, 1, 'websearch-agent-exe', 'aaas/websearch-agent-exe:latest',
        '{"22/tcp": 50022}', '{"path/to/work_dir": {"bind": "/root", "mode": "rw"}}',
        1, 'localhost', 50022, 'root', 'toor', '{}'
        );                            
    ''')
    
    # Insert task for agent
    cursor.execute('''
        INSERT INTO agent_tasks (task_id, agent_id, task_name, task_description) 
        VALUES ('task_001', 'agent_001', 'web_search', 'Perform a web search and gather information');
    ''')

    # Insert tools
    cursor.execute('''
        INSERT INTO tools (tool_id, tool_name, tool_description)
        VALUES ('tool_001', 'browser', 'Web browser for scraping data'), 
            ('tool_002', 'scraper', 'Data scraping tool');
    ''')

    # Associate tools with task
    cursor.execute('''
        INSERT INTO task_tools (task_id, tool_id)
        VALUES ('task_001', 'tool_001'), ('task_001', 'tool_002');
    ''')

    conn.commit()
    
    if close_conn:
        conn.close()
    
    print("Database initialized successfully!")

if __name__ == '__main__':
    initialize_db()
