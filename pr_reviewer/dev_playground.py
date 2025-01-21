from src.adapters.outbound.llm_openrouter import OpenRouterInstructorAIModel
from src.application.reviewer import FileReviewResponse
from src.adapters.outbound.pr_repo_github import GithubPrRepo
from dotenv import load_dotenv
import os


def github_pr_repo():
    key = os.getenv("GITHUB_ACCESS_TOKEN") or ""
    g = GithubPrRepo(key)
    pr = g.get("https://github.com/Dokploy/dokploy/pull/1158/files#diff-3a07c3a049898c3c20d8f5a2a2eca7be87cdbb9272a50377f4d6461ec29b35e1", 1158)
    for change in pr.file_changes:
        print("\n======================================================\n")
        print(change.file_name)
        print(change.patch)


def open_router_model():
    key = os.getenv("OPEN_ROUTER_API_KEY") or ""
    model = OpenRouterInstructorAIModel(api_key=key, model_name="gpt-4o-mini")
    res = model.sync_prompt("You are useful code reviewer, for given code review it", "var x = a / b", FileReviewResponse)
    print(res)


def main():
    load_dotenv()
    
    # uncomment the ones you want to play with
    
    # open_router_model()
    # github_pr_repo()


if __name__ == "__main__":
    main()
