from src.adapters.outbound.llm_openrouter import OpenRouterInstructorAIModel
from src.application.reviewer import FileReviewResponse
from src.adapters.outbound.pr_repo_github import GithubPrRepo
from src.application.reviewer_agentic import AgenticReviewer
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


def github_pr_repo():
    key = os.getenv("GITHUB_ACCESS_TOKEN") or ""
    url = "https://github.com/openai/openai-python/pull/2032"
    pr_no = 2032
    g = GithubPrRepo(key)
    pr = g.get(url, pr_no)
    print("pr: ", pr.base_ref, pr.head_ref)
    # res = g.get_file(url)


def open_router_model():
    key = os.getenv("OPEN_ROUTER_API_KEY") or ""
    model = OpenRouterInstructorAIModel(api_key=key, model_name="gpt-4o-mini")
    res = model.sync_prompt(
        "You are useful code reviewer, for given code review it",
        "var x = a / b",
        FileReviewResponse,
    )
    print(res)


def pr_agent():
    key = os.getenv("OPEN_ROUTER_API_KEY") or ""
    githubkey = os.getenv("GITHUB_ACCESS_TOKEN") or ""
    g = GithubPrRepo(githubkey)

    openai = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=SecretStr(key),
        model="gpt-3.5-turbo",
    )
    reviewer = AgenticReviewer(openai, g)
    pr = g.get("https://github.com/openai/openai-python/pull/2032", 2032)
    reviewer.review_pr(pr)


def main():
    load_dotenv()

    # uncomment the ones you want to play with

    # open_router_model()
    # github_pr_repo()
    pr_agent()


if __name__ == "__main__":
    main()
