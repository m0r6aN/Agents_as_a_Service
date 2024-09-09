# File: core/tasks/base_task.py

from abc import ABC, abstractmethod
import asyncio
from typing import Dict, List, Optional
import logging
import uuid
from enum import Enum

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"

class TaskBase(ABC):
    def __init__(
        self,
        name: str,
        description: str,
        tools: List[str],
        dependencies: Optional[List['TaskBase']] = None,
        retry_count: int = 3,
        timeout: Optional[int] = None,
        context: Optional[Dict[str, any]] = None
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.tools = tools
        self.dependencies = dependencies or []
        self.retry_count = retry_count
        self.timeout = timeout
        self.context = context or {}
        self.status = TaskStatus.PENDING
        self.result: Optional[any] = None
        self.error: Optional[str] = None

    def _dependencies_satisfied(self) -> bool:
        return all(dep.status == TaskStatus.COMPLETED for dep in self.dependencies)

    async def execute(self) -> any:
        attempts = 0
        self.status = TaskStatus.IN_PROGRESS
        while attempts < self.retry_count:
            try:
                logger.info(f"Starting task {self.name} with ID {self.id}. Retry {attempts + 1}/{self.retry_count}")
                
                if self.timeout:
                    self.result = await asyncio.wait_for(self.run(), timeout=self.timeout)
                else:
                    self.result = self.run()
                self.status = TaskStatus.COMPLETED
                return self.result
            except asyncio.TimeoutError:
                self.error = "Task timed out"
                self.status = TaskStatus.FAILED
                break
            except Exception as e:
                attempts += 1
                self.error = str(e)
                if attempts >= self.retry_count:
                    self.status = TaskStatus.FAILED
                    raise e

    @abstractmethod
    def run(self) -> any:
        pass
