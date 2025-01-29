from src.domain.pull_request import PullRequest
from src.domain.review import Review, Issue
from src.ports.reviewer import IPullRequestReviewer
from src.ports.pull_request_repo import IPullRequestRepo
from langchain.agents import AgentExecutor
from langchain_core.language_models import BaseLanguageModel
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from src.domain.review import FileReview
from langchain.output_parsers import PydanticOutputParser
from src.application.intelligence.models import CodeIssue
from src.application.intelligence.prompts import get_static_analysis_user_prompt
from src.application.intelligence.agents import (
    get_context_fetcher_agent,
    get_static_analysis_agent,
)


class AgentState(TypedDict):
    pr: PullRequest
    file_reviews: List[FileReview]


code_issue_output_parser = PydanticOutputParser(pydantic_object=List[CodeIssue])


class AgenticReviewer(IPullRequestReviewer):
    """
    Implements IPullRequestReviewer port.

    Features:
    1. Have a bot, so we can have a back and forth
    2. Review in a detailed way by having a tool to access repo
    3. Multi-agent, one agent to verify if the review is valid

    Approach:
    1. Use semgrep for security vulnerabilities, static analysis
    2. Fetch context and build ast for changes
    3. Code style enforcement agent
    4. Anti pattern agent
    5. Syntax validation agent
    """

    def __init__(self, llm: BaseLanguageModel, repo: IPullRequestRepo):

        # init agents
        static_analysis_agent_executor = get_static_analysis_agent(llm)
        context_fetcher_agent_executor = get_context_fetcher_agent(llm, repo)
        # anti_pattern_detection_agent
        # style_enforcement_agent

        # add more agents and build graph
        self.graph = self.build_graph(
            static_analysis_agent_executor, context_fetcher_agent_executor
        )

    def build_graph(
        self,
        static_analysis_agent_executor: AgentExecutor,
        context_fetcher_agent_executor: AgentExecutor,
    ):
        # build graph
        graph_builder = StateGraph(AgentState)

        def static_analysis(state: AgentState) -> AgentState:
            pr = state["pr"]
            for file in state["pr"].file_changes:
                _issues = static_analysis_agent_executor.invoke(
                    {
                        "pr_details": get_static_analysis_user_prompt(
                            pr.title, pr.description, file.patch
                        )
                    }
                )
                issues = code_issue_output_parser.parse(_issues["results"])
                review_issues: List[Issue] = []
                for issue in issues:
                    review_issues.append(
                        Issue(
                            type=issue.type,
                            line=issue.line_number,
                            description=issue.description,
                            suggestion=issue.suggestion,
                            severity=issue.severity,
                        )
                    )

                state["file_reviews"].append(
                    FileReview(
                        file_name=file.file_name,
                        issues=review_issues,
                    )
                )
            return state

        def context_fetcher(state: AgentState) -> AgentState:
            file_list: List[str] = []
            for file in state["pr"].file_changes:
                file_list.append(file.file_name)

            res = context_fetcher_agent_executor.invoke(
                {
                    "data": ",".join(file_list),
                },
            )
            # TODO: parse ast for head_ref and base_ref and run context rich review
            return state

        graph_builder.add_node(static_analysis)
        graph_builder.add_node(context_fetcher)

        graph_builder.add_edge(START, "static_analysis")
        graph_builder.add_edge("static_analysis", "context_fetcher")
        graph_builder.add_edge("context_fetcher", END)

        return graph_builder.compile()

    def review_pr(self, pr: PullRequest) -> Review:
        state = self.graph.invoke(input=AgentState(pr=pr, file_reviews=[]))
        return state["file_reviews"]
