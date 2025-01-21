from celery import Celery
from src.ports.task_execution import ITaskConsumer


def create_task(app:Celery, consumer: ITaskConsumer): 
    """ This is closure that helps dependency inversion of worker application 
        while being able to register the task function to celery """

    @app.task
    def task_function(task_id: int):
        # Use injected service
        consumer.on_task(task_id=task_id)

    return task_function
