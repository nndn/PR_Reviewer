from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from src.ports.pull_request_repo import IPullRequestRepo
from langchain_core.language_models import BaseLanguageModel
from src.application.intelligence.tools import (
    get_file_from_repo,
    get_repo_dir_structure,
)
from src.application.intelligence.prompts import get_static_analysis_system_prompt


def get_context_rich_reviewer_agent(llm: BaseLanguageModel, repo: IPullRequestRepo):
    tools = [
        get_file_from_repo.get_file_from_repo_tool(repo),
        get_repo_dir_structure.get_dir_structure_from_repo_tool(repo),
        # tree-sitter ast breakdown tool
    ]
    context_rich_reviewer_agent = create_tool_calling_agent(
        llm,
        tools=tools,
        prompt=ChatPromptTemplate(
            messages=[
                (
                    "system",
                    # add tree sitter tool commands here so that agent doesn't have to guess from import statements
                    """Analyze code changes for repo {repo_name} with auth_token {auth_token}
                    
                    1. Fetch file for the diff using get_file_from_repo tool
                    2. Fetch directory structure from get_dir_structure_from_repo tool
                    3. Figure out the main language of the current file
                    4. Figure out context of the code changes, using import statements and file structure,
                        fetch the file containing imported modules/packages
                    5. using the enriched context review the current code changes in the diff
                    
                    """
                    + get_static_analysis_system_prompt(),
                ),
                ("human", "\npr diffs: \n {pr_diffs} \n\n\n pr details: {pr_details}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        ),
        output_parser=code_issue_output_parser,  # type: ignore
    )

    return AgentExecutor(agent=context_rich_reviewer_agent, tools=tools)
