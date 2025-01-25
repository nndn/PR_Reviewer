from abc import ABC, abstractmethod
from typing import Optional
from src.domain.task import TaskStatus, Review, ReviewTask


class ITaskRepo(ABC):
    """Implementations for this interface should be in the adapter layer (outbound ports).
    Task repository manages storing and retrieving tasks"""

    @abstractmethod
    def add(
        self, repo_url: str, pr_number: int, auth_token: Optional[str] = None
    ) -> int:
        """insert a new task into repo"""
        pass

    @abstractmethod
    def get(self, task_id: int) -> ReviewTask:
        """get task details by id"""
        pass

    @abstractmethod
    def update(self, task_id: int, status: TaskStatus, result: Optional[Review] = None):
        """update task status and result for the given task_id"""
        pass
