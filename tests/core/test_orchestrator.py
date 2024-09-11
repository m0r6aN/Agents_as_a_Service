import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from core.agents.orchestration.orchestrator_agent import Orchestrator
from core.process.process_base import ProcessBase
from core.execution_context import ExecutionContext
from core.utils.task_handler import TaskHandler

class MockProcess(ProcessBase):
    def __init__(self, orchestrator):
        super().__init__(orchestrator)
        self.orchestrator = orchestrator
        self.define_agents()
        self.define_tasks()
        self.define_workflow()

    def define_agents(self):
        self.agents = {"agent_1": AsyncMock()}

    def define_tasks(self):
        self.tasks = {
            "task_1": {
                "agent": "agent_1",
                "action": "action_1",
                "input_data": {}
            }
        }

    def define_workflow(self):
        self.workflow = {
            "tasks": {
                "task_1": {
                    "agent": "agent_1",
                    "action": "action_1",
                    "input_data": {}
                }
            }
        }

    def get_start_task(self):
        return "task_1"

@pytest.mark.asyncio
async def test_orchestrator_executes_workflow():
    mock_agent = AsyncMock()
    mock_task_handler = MagicMock(spec=TaskHandler)
    mock_task_handler.execute_task.return_value = "success"

    orchestrator = Orchestrator()
    orchestrator.task_handler = mock_task_handler

    process = MockProcess(orchestrator=orchestrator)
    process.agents = {"agent_1": mock_agent}

    context = ExecutionContext()

    await orchestrator.execute(process, context)

    mock_task_handler.execute_task.assert_called_once_with(mock_agent, "action_1", {})
    assert "task_1" in context.completed_tasks
    assert context.get_state() == {"task_1": "success"}

@pytest.mark.asyncio
async def test_orchestrator_handles_task_exception():
    mock_agent = AsyncMock()
    mock_task_handler = MagicMock(spec=TaskHandler)
    mock_task_handler.execute_task.side_effect = Exception("Simulated Exception")

    orchestrator = Orchestrator()
    orchestrator.task_handler = mock_task_handler

    process = MockProcess(orchestrator=orchestrator)
    process.agents = {"agent_1": mock_agent}

    context = ExecutionContext()

    with pytest.raises(Exception) as exc_info:
        await orchestrator.execute(process, context)

    assert str(exc_info.value) == "Simulated Exception"
    mock_task_handler.execute_task.assert_called_once_with(mock_agent, "action_1", {})
    assert "task_1" not in context.completed_tasks
    assert context.get_state() == {}

@pytest.mark.asyncio
async def test_orchestrator_get_next_task():
    orchestrator = Orchestrator()
    
    workflow = {
        "tasks": {
            "task_1": {"dependencies": []},
            "task_2": {"dependencies": ["task_1"]},
            "task_3": {"dependencies": ["task_1", "task_2"]}
        }
    }
    
    context = ExecutionContext()
    
    # Initial state
    assert orchestrator.get_next_task(workflow, context) == "task_1"
    
    # After task_1 is completed
    context.update_state("task_1", "result_1")
    assert orchestrator.get_next_task(workflow, context) == "task_2"
    
    # After task_2 is completed
    context.update_state("task_2", "result_2")
    assert orchestrator.get_next_task(workflow, context) == "task_3"
    
    # After all tasks are completed
    context.update_state("task_3", "result_3")
    assert orchestrator.get_next_task(workflow, context) is None

# You might need to implement this method in your Orchestrator class
def test_orchestrator_are_dependencies_met():
    orchestrator = Orchestrator()
    
    context = ExecutionContext()
    context.update_state("task_1", "result_1")
    
    task_info = {"dependencies": ["task_1"]}
    assert orchestrator.are_dependencies_met(task_info, context) == True
    
    task_info = {"dependencies": ["task_1", "task_2"]}
    assert orchestrator.are_dependencies_met(task_info, context) == False
    
    context.update_state("task_2", "result_2")
    assert orchestrator.are_dependencies_met(task_info, context) == True