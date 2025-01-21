from celery import Celery
from src.application.worker import WorkerApplication


def create_task(app:Celery, worker: WorkerApplication): 

    @app.task
    def task_function(task_id: int):
        # Use injected service
        worker.on_task(task_id=task_id)

    return task_function
