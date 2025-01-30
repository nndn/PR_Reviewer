from langchain_core.tools import StructuredTool
from src.ports.pull_request_repo import IPullRequestRepo


class GetDirStructureFromRepoTool:
    """Retrieve a directory structure from repo details"""

    name = "get_dir_structure_for_repo"
    description = """Retrieves file content for given repo_name, auth_token
    
    Returns file structure of the repository with all the file names
    For input :
        ```
            dir_name
                subdir_name
                    ...
                filename.extension
        ```
        the path for the subdir_name should be dir_name/subdir_name
    """

    def __init__(self, repo: IPullRequestRepo):
        self.pr_repo = repo

    def run(self, repo_name: str, auth_token: str) -> str:
        return self.pr_repo.get_dir_structure(repo_name, auth_token)


def get_dir_structure_from_repo_tool(repo: IPullRequestRepo) -> StructuredTool:
    return StructuredTool(
        name="get_dir_structure_for_repo",
        description="""Retrieves file content for given repo_name, head_commit_sha and 
        
        :param path: string, the path of the file to get
    
            example:
            {
                "path": "src/application/server.py"
            }
    
        Returns raw content of the file.""",
        func=GetDirStructureFromRepoTool(repo).run,
    )
