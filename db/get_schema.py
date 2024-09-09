import sqlite3

def get_schema():
    conn = sqlite3.connect('Chinook.db')
    cursor = conn.cursor()
    
    # Fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema = {}
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        schema[table_name] = [column[1] for column in columns]  # Store just the column names
    
    conn.close()
    return schema

if __name__ == "__main__":
    get_schema()