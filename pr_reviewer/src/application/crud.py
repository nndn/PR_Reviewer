from logging import Logger
from typing import Optional, Callable, Tuple
from src.domain.task import Review, TaskStatus
from src.ports.crud_application import ICrudApplication
from src.ports.task_repo import ITaskRepo
from src.ports.task_execution import ITaskPublisher


class CrudApplication(ICrudApplication):

    def __init__(self, logger: Logger, task_repo:ITaskRepo, task_publisher:ITaskPublisher):
        self.logger = logger
        self.task_repo = task_repo
        self.task_publisher = task_publisher

    def add_review_task(self, repo_url: str, pr_number: int, auth_token: str | None=None) -> int:
        
        task_id = self.task_repo.add(repo_url, pr_number, auth_token)
        self.task_publisher.add_review_task(task_id=task_id)
        
        return task_id

    def get_review_status(self, task_id: int) -> TaskStatus:
        
        task = self.task_repo.get(task_id)
        return task.status

    def get_review_result(self, task_id: int) -> Tuple[TaskStatus, Optional[Review]]:
       
        task = self.task_repo.get(task_id)
        if task.status == TaskStatus.COMPLETED:
            return task.status, task.results
        return task.status, None
    
