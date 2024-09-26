from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# Create the engine
engine = create_engine("sqlite://localhost/query_agent.db")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))