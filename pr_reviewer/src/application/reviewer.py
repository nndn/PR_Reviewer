from typing import List
from pydantic import BaseModel, Field
from src.domain.pull_request import PullRequest
from src.domain.review import Review, ReviewSummary, FileReview, Issue, IssueType
from src.ports.reviewer import IPullRequestReviewer
from src.ports.ai import ILanguageModel


class CodeIssue(BaseModel):
    line_number: int = Field(..., description="line number where the issue was found, line_number will be present at start of each line of code")
    type: IssueType = Field(..., description="""keyword for the type of issue, it should always be one of the examples mentioned. 
                            type = 'style' implies that the issue is cosmetic and won't affect the problem itself, it only affects the readability """,
            examples=[IssueType.BUG, IssueType.IMPROVEMENT, IssueType.STYLE, IssueType.SUGGESTION, IssueType.WARNING])
    description: str = Field(..., description="""describes the issue in detail, summarize issue in first couple of sentence then explain. 
                             Total length shouldn't be more than 500 words and if could be explained with very few words should be done so""")
    suggestion: str = Field(..., description="write a suggestion to fix the described issue, should be concise and use fewer words. Should not be more than 500 words")
    severity: str = Field(..., description="keyword for severity of the issue, it should always be one of the examples mentioned",
            examples=["low", "medium", "high", "critical"])

    
def get_system_prompt() -> str:
    return f"""
You are PR-Reviewer. A useful llm agent that reviews Github pull requests.
Your task is to review given lines of code and provide concise, constructive and precise feedbacks.
You'll be finding issues in the code snippets, however it's fine to not find any issues.
Only respond with issues if you find any. Focus of the review should be on new code from context of old code,
new code lines will be appended with '+', old deleted code will be starting with '-', rest won't have either

example for a code diff is:

======
## File: 'src/file1.py'

@@ ... @@ def func1():
__new hunk__
11.  unchanged code line0
12.  unchanged code line1
13. +new code line2 added
14.  unchanged code line3
__old hunk__
 unchanged code line0
 unchanged code line1
-old code line2 removed
 unchanged code line3

@@ ... @@ def func2():
__new hunk__
 unchanged code line4
+new code line5 removed
 unchanged code line6

## File: 'src/file2.py'
...
======

- In the format above, the diff is organized into separate '__new hunk__' and '__old hunk__' sections for each code chunk. '__new hunk__' contains the updated code, while '__old hunk__' shows the removed code. If no code was removed in a specific chunk, the __old hunk__ section will be omitted.
- Each line will start with the line number, refer to it to get line number in the result
- Code lines are prefixed with symbols ('+', '-', ' '). The '+' symbol indicates new code added in the PR, the '-' symbol indicates code removed in the PR, and the ' ' symbol indicates unchanged code. \
 The review should address new code added in the PR code diff (lines starting with '+')
- When quoting variables, names or file paths from the code, use backticks (`) instead of single quote (').
"""


def get_user_prompt(pr_title:str, pr_description:str, patch: str) -> str:
    return f"""
each section below ends with '==================='

pull request title: 
===================
{pr_title}
===================

pull request description:
===================
{pr_description}
===================

review the code diff mentioned below:
===================
{patch}
===================
            """


class FileReviewResponse(BaseModel):
    issues: List[CodeIssue] = Field(default_factory=list, description="list of detected code issues")


class SimpleReviewer(IPullRequestReviewer):
    """ SimpleReviewer provides simple context independent reviews for code snippets in a PR"""

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
                get_system_prompt(),
                get_user_prompt(pr.title, pr.description, file.patch),
                response_type=FileReviewResponse)
            
            if len(file_review.issues) > 0:
                total_files += 1
            issues:List[Issue] = []
            for issue in file_review.issues:
                issues.append(Issue(type=issue.type, line=issue.line_number, description=issue.description, suggestion=issue.suggestion, severity=issue.severity))
                total_issues += 1
                if issue.severity == "critical":
                    critical_issues += 1
                
            file_reviews.append(FileReview(file_name=file.file_name, issues=issues))
        return Review(file_reviews, ReviewSummary(total_files, total_issues, 0))
