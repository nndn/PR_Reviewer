from celery import Celery
from typing import Callable
from src.ports.task_execution import ITaskPublisher


class CeleryTaskPublisher(ITaskPublisher):
    
    def __init__(self, task:Callable[[int], None]): 
        self.task = task
        
    def add_review_task(self, task_id: int):
        # task is a celery Task, it attaches type dynamically hence we ignore type error here
        self.task.delay(task_id)  # type: ignore
