import asyncio
from core.agents.orchestration.orchestrator_agent import Orchestrator
from processes.sql_nlp.sql_process import SQLProcess

async def main():
    # Assuming Orchestrator and SQLAgent are already defined
    orchestrator = Orchestrator()

    # Create SQLProcess instance
    sql_process = SQLProcess(orchestrator)

    # Define agents, tasks, and workflow for SQLProcess
    sql_process.define_agents()
    sql_process.define_tasks()
    sql_process.define_workflow()

    # Example natural language query to SQL process flow
    natural_language_query = "Show me all customers from the USA."

    # This triggers the Orchestrator to execute the workflow
    context = {"query": natural_language_query}  # Initial context

    try:
        await orchestrator.execute(sql_process, context)
    except Exception as e:
        print(f"Error during workflow execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())
