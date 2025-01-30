from typing import List
from pydantic import BaseModel, Field
from src.domain.pull_request import PullRequest
from src.domain.review import Review, ReviewSummary, FileReview, Issue
from src.ports.reviewer import IPullRequestReviewer
from src.ports.ai import ILanguageModel
from src.application.intelligence.prompts import (
    get_static_analysis_system_prompt,
    get_static_analysis_user_prompt,
)
from src.application.intelligence.models import CodeIssue


class FileReviewResponse(BaseModel):
    issues: List[CodeIssue] = Field(
        default_factory=list, description="list of detected code issues"
    )


class SimpleReviewer(IPullRequestReviewer):
    """SimpleReviewer provides simple context independent reviews for code snippets in a PR"""

    def __init__(self, llm: ILanguageModel):
        self.llm = llm

    def review_pr(self, pr: PullRequest) -> Review:
        file_reviews: List[FileReview] = []
        total_files = 0
        total_issues = 0
        critical_issues = 0

        # TODO: batch multiple files to same request, take into consideration total tokens
        for file in pr.file_changes:

            file_review = self.llm.sync_prompt(
                get_static_analysis_system_prompt(),
                get_static_analysis_user_prompt(pr.title, pr.description, file.patch),
                response_type=FileReviewResponse,
            )

            if len(file_review.issues) > 0:
                total_files += 1
            issues: List[Issue] = []
            for issue in file_review.issues:
                issues.append(
                    Issue(
                        type=issue.type,
                        line=issue.line_number,
                        description=issue.description,
                        suggestion=issue.suggestion,
                        severity=issue.severity,
                    )
                )
                total_issues += 1
                if issue.severity == "critical":
                    critical_issues += 1

            file_reviews.append(FileReview(file_name=file.file_name, issues=issues))
        return Review(
            file_reviews, ReviewSummary(total_files, total_issues, critical_issues)
        )
