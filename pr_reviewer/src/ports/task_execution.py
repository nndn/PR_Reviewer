from abc import ABC, abstractmethod
from src.domain.task import ReviewTask


class ITaskConsumer(ABC):
    
    @abstractmethod
    def on_review_task_received(self, task: ReviewTask):
        pass
    
    @abstractmethod
    def start(self):
        pass


class ITaskPublisher(ABC):
    
    @abstractmethod
    def add_review_task(self, task_id: int):
        pass
