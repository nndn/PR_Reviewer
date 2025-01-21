from abc import ABC, abstractmethod
from src.domain.pull_request import PullRequest
from src.domain.review import Review


class IPullRequestReviewer(ABC): 
    
    @abstractmethod
    def review_pr(self, pr:PullRequest) -> Review:
        pass
