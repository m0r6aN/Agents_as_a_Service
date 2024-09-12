import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from core.agents.orchestration.orchestrator_agent import Orchestrator
from core.utils.db_interactions import DatabaseClient
from core.agent import Agent
from core.execution_context import ExecutionContext
from core.process.process_base import ProcessBase

class TestOrchestrator(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.orchestrator = Orchestrator()
        self.orchestrator.db_client = MagicMock(DatabaseClient)

        # Define the necessary mock methods for db_client
        self.orchestrator.db_client.get_agent_config = AsyncMock()
        self.orchestrator.db_client.get_task_for_agent = AsyncMock()
        self.orchestrator.db_client.get_tools_for_task = AsyncMock()
        self.orchestrator.db_client.save_agent = AsyncMock()
        self.orchestrator.db_client.save_task = AsyncMock()

    async def test_create_agent_from_config(self):
        # Mock the agent configuration from the database
        mock_agent_config = {
            "agent_id": "agent_001",
            "chat_model": "gpt-4",
            "utility_model": "davinci-003",
            "embeddings_model": "text-embedding-ada-002",
            "prompts_subdir": "prompts/web_search",
            "memory_subdir": "memory/web_search",
            "knowledge_subdir": "knowledge/web_search"
        }
        self.orchestrator.db_client.get_agent_config.return_value = mock_agent_config

        # Run the find_or_create_agent method, assuming no existing agent is found
        agent = await self.orchestrator.find_or_create_agent("web_search")

        # Ensure agent creation from config was called
        self.orchestrator.db_client.get_agent_config.assert_called_once_with("web_search")
        self.orchestrator.db_client.save_agent.assert_called_once_with(agent)

        # Check that the agent was correctly created from the config
        self.assertEqual(agent.agent_id, "agent_001")
        self.assertEqual(agent.config["chat_model"], "gpt-4")
    
    async def test_task_and_tools_assigned(self):
        # Mock agent config and task details from the database
        mock_agent_config = {
            "agent_id": "agent_001",
            "chat_model": "gpt-4",
            "utility_model": "davinci-003"
        }
        mock_task_config = {
            "task_id": "task_001",
            "task_name": "web_search",
            "task_description": "Perform a web search"
        }
        mock_tools = [{"tool_name": "browser"}, {"tool_name": "scraper"}]

        self.orchestrator.db_client.get_agent_config.return_value = mock_agent_config
        self.orchestrator.db_client.get_task_for_agent.return_value = mock_task_config
        self.orchestrator.db_client.get_tools_for_task.return_value = mock_tools

        # Run the find_or_create_agent method and get the assigned task and tools
        agent = await self.orchestrator.find_or_create_agent("web_search")
        tools = self.orchestrator.get_tools_for_task("task_001")

        # Ensure tools were correctly assigned to the task
        self.assertEqual(tools, ["browser", "scraper"])

    async def test_task_assignment(self):
        # Mock task and agent assignment
        mock_task_config = {
            "task_id": "task_001",
            "agent_id": "agent_001",
            "task_name": "web_search",
            "task_description": "Perform a web search"
        }

        self.orchestrator.db_client.get_task_for_agent.return_value = mock_task_config

        # Ensure task is correctly assigned to agent
        task = self.orchestrator.db_client.get_task_for_agent("agent_001")
        self.assertEqual(task["task_name"], "web_search")
        self.assertEqual(task["task_id"], "task_001")
        self.assertEqual(task["agent_id"], "agent_001")

    @patch('uuid.uuid4')
    async def test_find_or_create_agent_new(self, mock_uuid):
        # Mock UUID generation to always return 'agent_2'
        mock_uuid.return_value = "agent_2"
        
        # Simulate a new agent creation
        self.orchestrator.db_client.agent_exists.return_value = False
        agent_config = {"agent_id": None, "agent_name": "New Agent"}
        
        # Mock the newly created agent and ensure it has agent_name and agent_id
        mock_agent = MagicMock(Agent)
        mock_agent.agent_name = "New Agent"
        mock_agent.agent_id = "agent_2"  # Ensure this matches the mocked UUID
        self.orchestrator.db_client.save_agent.return_value = mock_agent

        # Run the function to test agent creation
        agent = await self.orchestrator.find_or_create_agent("web_search")

        # Verify that save_agent was called and the agent has the expected attributes
        self.orchestrator.db_client.save_agent.assert_called_once()
        self.assertEqual(agent.agent_name, "New Agent")
        self.assertEqual(agent.agent_id, "agent_2")

    async def test_are_dependencies_met(self):
        # Mock context to simulate task dependency completion
        mock_context = MagicMock(ExecutionContext)
        mock_context.get_state.side_effect = lambda dep: "completed" if dep == "task_1" else None

        task_info = {"dependencies": ["task_1"]}
        result = self.orchestrator.are_dependencies_met(task_info, mock_context)
        
        self.assertTrue(result)

    async def test_are_dependencies_not_met(self):
        # Mock context where dependencies are not completed
        mock_context = MagicMock(ExecutionContext)
        mock_context.get_state.side_effect = lambda dep: None

        task_info = {"dependencies": ["task_1"]}
        result = self.orchestrator.are_dependencies_met(task_info, mock_context)
        
        self.assertFalse(result)

    async def test_execute_with_dependent_tasks(self):
        # Mock context and agents
        mock_context = MagicMock(ExecutionContext)
        mock_context.get_state.return_value = "completed"

        # Mock agent with necessary attributes
        mock_agent = AsyncMock(Agent)
        mock_agent.agent_id = "agent_1"  # Manually set agent_id
        mock_agent.agent_name = "Agent 1"  # Set agent_name
        self.orchestrator.create_or_load_agent = AsyncMock(return_value=mock_agent)

        mock_process = MagicMock(ProcessBase)
        mock_process.workflow = {
            "tasks": {
                "task_1": {
                    "agent_config": {"agent_name": "Agent 1"},
                    "action": "do_something",
                    "input_data": {}
                }
            }
        }

        await self.orchestrator.execute(mock_process, mock_context)

        # Assert that agent was called with correct task
        mock_agent.execute_task.assert_awaited_once_with("do_something", {})

        # Check that the task was saved to the database
        self.orchestrator.db_client.save_task.assert_called_once()

    async def test_get_next_task(self):
        # Mock tasks and context for a simple workflow
        tasks = {
            "task_1": {"dependencies": []},
            "task_2": {"dependencies": ["task_1"]}
        }

        mock_context = MagicMock(ExecutionContext)
        mock_context.get_state.return_value = "completed"

        task_name, task_info = self.orchestrator.get_next_task(tasks, mock_context)

        self.assertEqual(task_name, "task_1")

    async def test_task_execution_with_result_persistence(self):
        # Mock the context and agent
        mock_context = MagicMock(ExecutionContext)
        mock_agent = AsyncMock(Agent)
        mock_agent.agent_id = "agent_1"  # Manually set agent_id
        mock_agent.agent_name = "Agent 1"  # Set agent_name
        self.orchestrator.create_or_load_agent = AsyncMock(return_value=mock_agent)

        mock_process = MagicMock(ProcessBase)
        mock_process.workflow = {
            "tasks": {
                "task_1": {
                    "agent_config": {"agent_name": "Agent 1"},
                    "action": "do_something",
                    "input_data": {}
                }
            }
        }

        # Mock task execution result
        mock_agent.execute_task.return_value = True
        await self.orchestrator.execute(mock_process, mock_context)

        # Check that task result is persisted
        self.orchestrator.db_client.save_task.assert_called_once_with({
            "agent_id": "agent_1",
            "task_name": "task_1",
            "task_status": "completed",
            "result": True
        })