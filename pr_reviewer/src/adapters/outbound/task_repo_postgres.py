from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import String, Integer, DateTime, JSON, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.sql import func
from src.domain.task import TaskStatus, Review, ReviewTask
from src.domain.review import ReviewSummary
from src.ports.task_repo import ITaskRepo
from src.domain.exceptions import ResourceNotFound
from dataclasses import asdict


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    repo_url: Mapped[str] = mapped_column(String(255))
    pr_number: Mapped[int] = mapped_column(Integer)
    auth_token: Mapped[str] = mapped_column(String(255))
    status: Mapped[TaskStatus] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.utcnow()
    )
    results = mapped_column(JSON)

    def set_results(self, results: Review):
        self.results = asdict(results)

    def get_results(self):
        return Review(**self.results)

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, repo={self.repo_url!r})"


class PostgresTaskRepo(ITaskRepo):

    def __init__(self, dsn: str):
        self.db = create_engine(url=dsn)

    def add(
        self, repo_url: str, pr_number: int, auth_token: Optional[str] = None
    ) -> int:
        task_id = 0
        with Session(self.db) as session:
            task = Task(
                repo_url=repo_url,
                pr_number=pr_number,
                status=TaskStatus.PENDING,
                auth_token=auth_token or "",
            )
            task.set_results(Review([], ReviewSummary(0, 0, 0)))
            session.add(task)
            session.commit()
            task_id = task.id
        return task_id

    def get(self, task_id: int) -> ReviewTask:
        with Session(self.db) as session:
            stmt = select(Task).where(Task.id == task_id)
            res = session.scalar(stmt)
            if res == None:
                raise ResourceNotFound("task not found")

            return ReviewTask(
                id=res.id,
                repo_url=res.repo_url,
                pr_number=res.pr_number,
                auth_token=res.auth_token,
                status=res.status,
                created_at=res.created_at,
                results=res.get_results(),
            )

    def update(
        self, task_id: int, status: TaskStatus, result: Optional[Review] = None
    ) -> None:
        with Session(self.db) as session:
            stmt = select(Task).where(Task.id == task_id)
            task = session.scalar(stmt)
            if task is None:
                raise ResourceNotFound("task not found")

            task.status = status
            if result is not None:
                task.set_results(result)
            session.commit()
