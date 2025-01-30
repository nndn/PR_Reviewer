from langchain_core.tools import StructuredTool
from src.ports.pull_request_repo import IPullRequestRepo


class GetFileFromRepoTool:
    """Retrieve a file for a given path and repo details"""

    name = "get_file_from_by_path"
    description = """Retrieves file content for given repo_name, head_commit_sha and 
    :param path: string, the path of the file to get
    
        example:
        {
            "path": "src/application/server.py"
        }
    
    Returns raw content of the file.
    """

    def __init__(self, repo: IPullRequestRepo):
        self.pr_repo = repo

    def _get_file(self, repo_name: str, branch: str, path: str, auth_token: str) -> str:
        return self.pr_repo.get_file(repo_name, branch, path, auth_token)

    # TODO: try to just pass path here, rest can be injected somehow
    def run(self, repo_name: str, branch: str, path: str, auth_token: str) -> str:
        return self._get_file(repo_name, branch, path, auth_token)


def get_file_from_repo_tool(repo: IPullRequestRepo) -> StructuredTool:
    return StructuredTool(
        name="get_file_from_repo",
        description="""Retrieves file content for given repo_name, head_commit_sha and 
        
        :param path: string, the path of the file to get
    
            example:
            {
                "path": "src/application/server.py"
            }
    
        Returns raw content of the file.""",
        func=GetFileFromRepoTool(repo).run,
    )
