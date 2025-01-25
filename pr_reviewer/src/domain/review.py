from dataclasses import dataclass
from enum import Enum
from typing import List


class IssueType(str, Enum):
    BUG = "bug"
    STYLE = "style"
    IMPROVEMENT = "improvement"
    SUGGESTION = "suggestion"
    WARNING = "warning"


@dataclass
class Issue:
    type: IssueType
    line: int
    description: str
    suggestion: str
    severity: str


@dataclass
class FileReview:
    file_name: str
    issues: List[Issue]


@dataclass
class ReviewSummary:
    total_files: int
    total_issues: int
    critical_issues: int


@dataclass
class Review:
    files: List[FileReview]
    summary: ReviewSummary
