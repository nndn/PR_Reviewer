import uvicorn
import os
from dotenv import load_dotenv
from src.adapters.inbound.crud_fastapi import CrudFastapiAdapter
from src.application.crud import CrudApplication
from src.utils.logger import get_logger
from src.application.worker import WorkerApplication
from src.utils.celery_task_closure import create_task
from celery import Celery
from src.adapters.outbound.task_repo_postgres import PostgresTaskRepo
from src.adapters.outbound.pr_repo_github import GithubPrRepo
from src.adapters.outbound.llm_openrouter import OpenRouterInstructorAIModel
from src.application.reviewer import SimpleReviewer
from src.adapters.outbound.task_publisher_celery import CeleryTaskPublisher
import threading

""" server runs the entire backend, it runs the crud apis aswell as background worker in
    a seperate thread. Application however is modular and if we decide to move away from
    celery we can run out worker as a seperate service """


def main():
    load_dotenv()
    # isDev = os.getenv("ENV") == "development"
    
    logger = get_logger()
    
    # inject dependencies into worker application
    github_auth_token = os.getenv("GITHUB_ACCESS_TOKEN") or ""
    pr_repo = GithubPrRepo(github_auth_token)
    
    postgres_dsn = os.getenv("POSTGRES_DSN") or "postgresql://postgres:password@localhost:5432/pr_reviewer"
    task_repo = PostgresTaskRepo(postgres_dsn)
    
    open_router_api_key = os.getenv("OPEN_ROUTER_API_KEY") or ""
    model = OpenRouterInstructorAIModel(open_router_api_key, "gpt-4o-mini")
    
    reviewer = SimpleReviewer(model)
    
    worker_app = WorkerApplication(logger=logger, pr_repo=pr_repo, task_repo=task_repo, reviewer=reviewer)
    
    redis_conn_string = os.getenv("REDIS_CONN_STRING") or "redis://localhost:6379"
    celery_app = Celery('tasks', broker=redis_conn_string + "/0" , backend=redis_conn_string + "/1")
    run_task = create_task(celery_app, worker_app)
    celery_app.register_task(run_task)
    
    worker_thread = threading.Thread(
        target=celery_app.worker_main,
        args=(['worker', '-l', 'info'],)
    )
    worker_thread.daemon = True
    worker_thread.start()
    
    # inject application into http server implementation
    task_publisher = CeleryTaskPublisher(run_task)
    app = CrudApplication(logger, task_repo, task_publisher)
    crud_fastapi_adapter = CrudFastapiAdapter(app).get_router()
    
    # start server
    host = os.getenv("CRUD_SERVER_HOST") or "127.0.0.1"
    port = os.getenv("CRUD_SERVER_PORT") or "8080"
    
    logger.info("Starting CRUD server...")
    
    uvicorn.run(crud_fastapi_adapter, host=host, port=int(port))


if __name__ == "__main__":
    main()

