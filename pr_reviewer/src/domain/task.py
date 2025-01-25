from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime
from src.domain.review import Review


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ReviewTask:
    id: int
    repo_url: str
    pr_number: int
    auth_token: str
    status: TaskStatus
    created_at: datetime
    results: Optional[Review] = None
