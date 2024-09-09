
# File: core/actions/sqlite_actions.py

import csv

import logging
import sqlite3

import requests
import sqlparse

async def run_sql_return_csv(sql_query, database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    # Execute the SQL query
    cursor.execute(sql_query)
    data = cursor.fetchall()
    
    # Convert to CSV
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    conn.close()
    return "CSV generated: output.csv"

async def run_sql_return_rows(sql_query, database_path):
        # Connect to a database and execute the SQL query
        conn = sqlite3.connect(database_path)  # Update with your DB connection
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()  # Fetch all results from the executed query
        conn.close()
        return results

def validate_sql(sql_query):
    parsed = sqlparse.parse(sql_query)
    
    # Check for potentially dangerous SQL operations (like DROP, DELETE, etc.)
    if any([str(token).upper() in ["DROP", "DELETE"] for token in parsed[0].tokens]):
        raise ValueError("Potentially dangerous SQL operation detected!")
    
    return True

import requests

async def generate_sql(self, natural_language_query):
    # POST to the /generate_sql endpoint to get the SQL query
    url = "http://localhost:9000/generate_sql/"
    payload = {"text": natural_language_query}

    try:
        # Set a timeout of 10 seconds
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()  # Parse the JSON response

        # Extract the SQL query from the response data
        sql_query = data.get("sql")
        if not sql_query:
            raise ValueError("No SQL query returned from the model.")
        
        return sql_query

    except requests.exceptions.Timeout:
        self.logger.error("Request timed out.")
        raise
    except requests.exceptions.RequestException as e:
        self.logger.error(f"Failed to generate SQL: {e}")
        raise
