from logging import Logger
from src.domain.task import ReviewTask, TaskStatus
from src.ports.pull_request_repo import IPullRequestRepo
from src.ports.task_repo import ITaskRepo
from src.ports.reviewer import IPullRequestReviewer
from src.ports.task_execution import ITaskConsumer
from retry import retry


class WorkerApplication(ITaskConsumer):

    def __init__(
        self,
        logger: Logger,
        pr_repo: IPullRequestRepo,
        task_repo: ITaskRepo,
        reviewer: IPullRequestReviewer,
    ):
        self.logger = logger
        self.pr_repo = pr_repo
        self.task_repo = task_repo
        self.reviewer = reviewer

    @retry(tries=3)
    def try_task(self, task_id: int):
        self.logger.info(f"trying task_id: {task_id}")
        self.task_repo.update(task_id, TaskStatus.PROCESSING)
        task = self.task_repo.get(task_id)
        pr = self.pr_repo.get(task.repo_url, task.pr_number, auth_token=task.auth_token)

        # pr review logic
        review = self.reviewer.review_pr(pr)

        self.task_repo.update(task.id, TaskStatus.COMPLETED, review)

    def on_task(self, task_id: int):
        try:
            self.try_task(task_id)
        except:
            self.task_repo.update(task_id, TaskStatus.FAILED)
