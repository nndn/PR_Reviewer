from typing import Optional, List
from github import Github
from github import Auth
from src.ports.pull_request_repo import IPullRequestRepo
from src.domain.pull_request import PullRequest, Assignee, FileChanges
import re

MAX_FILE_CHANGES_CHAR_SIZE = 10000


def extract_line_number(text) -> int:
    match = re.search(r"@@ -\s*(\d+)", text)
    return int(match.group(1)) if match else 0


def insert_line_numbers_to_patch(text: str, start_line: int) -> str:
    lines = text.splitlines()
    numbered_lines: list[str] = []
    i = start_line
    for line in lines:
        if line[0] != "-":
            numbered_lines.append(f"{i}. {line}")
            i += 1
    return "\n".join(numbered_lines)


class GithubPrRepo(IPullRequestRepo):

    def __init__(self, auth_token: str):
        auth = Auth.Token(auth_token)
        self.github = Github(auth=auth)

    def get(
        self, repo_url: str, pr_number: int, auth_token: Optional[str] = None
    ) -> PullRequest:

        # use the use auth token if passed, otherwise default to one that has public access
        github = self.github
        if auth_token is not None and auth_token != "":
            auth = Auth.Token(auth_token)
            github = Github(auth=auth)

        # break down owner and repo name
        url_parts = repo_url.split("github.com/")
        splits = url_parts[1].split("/")
        owner = splits[0]
        repo_name = splits[1]

        repo = github.get_repo(f"{owner}/{repo_name}")
        pr = repo.get_pull(pr_number)

        assignees: List[Assignee] = []
        for assignee in pr.assignees:
            assignees.append(Assignee(name=assignee.name, email=assignee.email))

        # fetch file changes from paginated api
        # TODO: filter images/ other non code resources etc
        file_changes: List[FileChanges] = []
        curr_page_no = 0
        curr_page = pr.get_files().get_page(curr_page_no)
        while len(curr_page) > 0:
            for file in curr_page:

                if len(file.patch) > 0 and len(file.patch) < MAX_FILE_CHANGES_CHAR_SIZE:
                    line_number = extract_line_number(file.patch)
                    patch = insert_line_numbers_to_patch(file.patch, line_number - 1)
                    file_changes.append(
                        FileChanges(
                            patch=patch,
                            file_name=file.filename,
                            patch_start_line_number=line_number,
                        )
                    )
            curr_page_no += 1
            curr_page = pr.get_files().get_page(curr_page_no)

        return PullRequest(
            assignees=assignees,
            title=pr.title,
            description=pr.body,
            file_changes=file_changes,
        )
