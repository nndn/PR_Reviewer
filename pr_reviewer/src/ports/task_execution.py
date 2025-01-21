from abc import ABC, abstractmethod
from src.domain.task import ReviewTask

""" Consumer and Publisher can sit on different service, that's why they are seperated """


class ITaskConsumer(ABC):
    """ Worker implements this interface in application layer """
    
    @abstractmethod
    def on_task(self, task_id: int):
        """ Run the review task """
        pass


class ITaskPublisher(ABC):
    """ Implementations for this interface should be in the adapter layer (outbound ports).
        This Publisher is used to publish the background task to the queue """
    
    @abstractmethod
    def add_review_task(self, task_id: int):
        """ Add the task_id to the queue, we just send the id because input here needs
            to be serialized/deserialized as it may move through whatever transport protocol
            the implementation uses """
        pass
