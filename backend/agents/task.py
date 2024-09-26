from typing import List, Dict, Any, Callable
from enum import Enum

class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"

class Task:
    def __init__(self, 
                 task_id: str,
                 task_name: str,
                 task_description: str,
                 capabilities: List[str],
                 function: Callable,
                 dependencies: List[str] = None,
                 tools: List[str] = None,
                 retry_count: int = 3,
                 timeout: int = 300,
                 context: Dict[str, Any] = None,
                 status: TaskStatus = TaskStatus.PENDING,
                 version: str = '1.0',
                 requires_tool: bool = False,
                 tool_name: str = None,
                 tool_description: str = None,
                 tool_code: str = None,
                 args: List[Any] = None,
                 kwargs: Dict[str, Any] = None):
        
        self.task_id = task_id
        self.task_name = task_name
        self.task_description = task_description
        self.capabilities = capabilities
        self.function = function
        self.dependencies = dependencies or []
        self.tools = tools or []
        self.retry_count = retry_count
        self.timeout = timeout
        self.context = context or {}
        self.status = status
        self.version = version
        self.requires_tool = requires_tool
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_code = tool_code
        self.args = args or []
        self.kwargs = kwargs or {}

    def update_status(self, new_status: TaskStatus) -> None:
        self.status = new_status

    def add_dependency(self, dependency_id: str) -> None:
        if dependency_id not in self.dependencies:
            self.dependencies.append(dependency_id)

    def add_tool(self, tool_id: str) -> None:
        if tool_id not in self.tools:
            self.tools.append(tool_id)

    def __str__(self) -> str:
        return f"Task(id={self.task_id}, name={self.task_name}, status={self.status.value})"

    def __repr__(self) -> str:
        return self.__str__()