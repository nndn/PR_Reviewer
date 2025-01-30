from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel
from src.ports.pull_request_repo import IPullRequestRepo
from src.application.intelligence.tools import (
    get_fetch_file_tool,
    get_semgrep_static_analysis_tool,
)
from src.application.intelligence.prompts import (
    get_static_analysis_system_prompt,
)


def get_static_analysis_agent(llm: BaseLanguageModel):
    tools = [get_semgrep_static_analysis_tool()]
    static_analysis_agent = create_tool_calling_agent(
        llm,
        tools=tools,
        prompt=ChatPromptTemplate(
            messages=[
                (
                    "system",
                    get_static_analysis_system_prompt()
                    + """
                    Use the get_semgrep_static_analysis_tool to get static analysis of the code
                    snippet. Review, build on the result and respond with necessary updates
                    """,
                ),
                ("human", "{pr_details}"),
                ("placeholder", "{agent_scratchpad}"),
            ],
        ),
        output_parser=code_issue_output_parser,  # type: ignore
    )

    return AgentExecutor(agent=static_analysis_agent, tools=tools)


def get_context_fetcher_agent(llm: BaseLanguageModel, repo: IPullRequestRepo):
    tools = [get_fetch_file_tool(repo)]
    context_fetcher_agent = create_tool_calling_agent(
        llm,
        tools=tools,
        prompt=ChatPromptTemplate(
            messages=[
                (
                    "system",
                    """use fetch_file tool to fetch files mentioned in the data,
                        
                        """,
                ),
                ("human", "data: {data}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        ),
        output_parser=code_issue_output_parser,  # type: ignore
    )

    return AgentExecutor(agent=context_fetcher_agent, tools=tools)
