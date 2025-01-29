from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Assignee:
    name: Optional[str]
    email: Optional[str]


@dataclass
class FileChanges:
    file_name: str
    patch: str
    patch_start_line_number: int


@dataclass
class PullRequest:
    assignees: List[Assignee]
    title: str
    description: str
    file_changes: List[FileChanges]
    base_repo: str
    head_repo: str
    base_ref: str
    head_ref: str
