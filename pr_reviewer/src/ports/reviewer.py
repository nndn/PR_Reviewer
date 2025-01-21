from abc import ABC, abstractmethod
from src.domain.pull_request import PullRequest
from src.domain.review import Review


class IPullRequestReviewer(ABC): 
    """ Implementation for this interface should be in the application layer.
        This could be thought of as a sub-application that sits inside the worker app.
        Although not necessary now this could be very useful as we improve our review strategy or 
        add completely new kinds of reviewer applications (for example: RAG based context rich reviews) """
    
    @abstractmethod
    def review_pr(self, pr:PullRequest) -> Review:
        """ For a given pr we return the review, this is a blocking call """
        pass
