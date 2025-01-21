from abc import ABC, abstractmethod
from typing import Optional, Tuple
from src.domain.task import TaskStatus
from src.domain.review import Review


class ICrudApplication(ABC):
    """ Implementation for this interface should be in the application layer.
        Inbound ports (http / grpc / command line) can use this interface to implement
        respective protocols for serving the application """
    
    @abstractmethod
    def add_review_task(self, repo_url: str, pr_number: int, auth_token: Optional[str]=None) -> int:
        """ add_review_job accepts pr details and creates a task for its review, returns the resulting task_id"""
        pass
    
    @abstractmethod
    def get_review_status(self, task_id: int) -> TaskStatus:
        """ get_review_status returns the status for the given task_id """
        pass
    
    @abstractmethod
    def get_review_result(self, task_id: int) -> Tuple[TaskStatus, Optional[Review]]:
        """ get_review_result returns the result for the given task_id if completed, None otherwise """
        pass
