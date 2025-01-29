from src.ports.pull_request_repo import IPullRequestRepo
from langchain.tools import tool
from pydantic import BaseModel, Field
import subprocess


class FetchFileInput(BaseModel):
    path: str = Field(description="path of the file to fetch")
    branch: str = Field(description="""name of the branch""")
    repo_name: str = Field(description="""name of the repo""")
    auth_token: str = Field(description="auth token")


def get_fetch_file_tool(repo: IPullRequestRepo):

    @tool
    def fetch_file(ip: FetchFileInput):
        """fetch file for the given path"""

        return repo.get_file(ip.repo_name, ip.branch, ip.path, ip.auth_token)

    return fetch_file


class StaticAnalysisInput(BaseModel):
    path: str = Field(description="path of the file to fetch")
    code_snippet: str = Field(description="snippet of code that needs to analyzed")


def get_semgrep_static_analysis_tool():

    @tool
    def static_analysis(ip: StaticAnalysisInput):
        """
        runs semgrep static analysis for given code snippet
        returns the issue in the snippet
        """
        result = subprocess.run(
            [ip.code_snippet, "|", "semgrep", "scan", "--config", "auto", "-"],
            capture_output=True,
            text=True,
        )
        return result

    return static_analysis
