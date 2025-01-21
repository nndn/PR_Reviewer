from typing import Optional, Dict, Any
from pydantic import BaseModel
from src.domain.review import Review
from src.domain.task import TaskStatus


class HealthCheck(BaseModel):
    status: str = "OK"

    
class AnalyzePrRequest(BaseModel):
    repo_url: str 
    pr_number: int
    github_token: Optional[str] = None
    
    
class AnalyzePrResponse(BaseModel):
    accepted: bool
    repo_url: str
    task_id: Optional[int] = None


class TaskStatusResponse(BaseModel):
    task_id:int
    status: TaskStatus


class TaskResultResponse(BaseModel):
    task_id: int
    status: TaskStatus
    results: Optional[Dict[str, Any]] = None

