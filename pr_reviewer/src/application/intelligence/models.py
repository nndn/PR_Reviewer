from pydantic import BaseModel, Field
from src.domain.review import IssueType


class CodeIssue(BaseModel):
    line_number: int = Field(
        ...,
        description="line number where the issue was found, line_number will be present at start of each line of code",
    )
    type: IssueType = Field(
        ...,
        description="""keyword for the type of issue, it should always be one of the examples mentioned. 
                            type = 'style' implies that the issue is cosmetic and won't affect the problem itself, it only affects the readability """,
        examples=[
            IssueType.BUG,
            IssueType.IMPROVEMENT,
            IssueType.STYLE,
            IssueType.SUGGESTION,
            IssueType.WARNING,
        ],
    )
    description: str = Field(
        ...,
        description="""describes the issue in detail, summarize issue in first couple of sentence then explain. 
                             Total length shouldn't be more than 500 words and if could be explained with very few words should be done so""",
    )
    suggestion: str = Field(
        ...,
        description="write a suggestion to fix the described issue, should be concise and use fewer words. Should not be more than 500 words",
    )
    severity: str = Field(
        ...,
        description="keyword for severity of the issue, it should always be one of the examples mentioned",
        examples=["low", "medium", "high", "critical"],
    )
