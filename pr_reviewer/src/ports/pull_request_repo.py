from abc import ABC, abstractmethod
from typing import Optional
from src.domain.pull_request import PullRequest


class IPullRequestRepo(ABC):
    """Implementations for this interface should be in the adapter layer (outbound ports).
    Pull Request repository manages retrieving of pull request details"""

    @abstractmethod
    def get(
        self, repo_url: str, pr_number: int, auth_token: Optional[str] = None
    ) -> PullRequest:
        """get accepts repo_url and pr number to query for pr details"""
        pass

    @abstractmethod
    def get_file(
        self, repo_str: str, branch: str, path: str, auth_token: Optional[str] = None
    ) -> str:
        """get a file in a branch"""
        pass
