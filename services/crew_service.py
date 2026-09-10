"""CrewAI application service and agent orchestration."""

from __future__ import annotations

import os
import time
from typing import Any

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from tools.mcp_tools import accounts_tool, services_tool, transactions_tool

MODEL_NAME = "openai/gpt-oss-120b"
MAX_RPM = 900
load_dotenv()


def _is_rate_limit_error(error: BaseException) -> bool:
    text = str(error).lower()
    return "429" in text or "rate limit" in text or "too many requests" in text


@retry(
    retry=retry_if_exception(_is_rate_limit_error),
    wait=wait_exponential(multiplier=1, min=2, max=12),
    stop=stop_after_attempt(4),
    reraise=True,
)
def create_llm() -> LLM:
    """Create the Groq chat model for the free-tier OSS model."""
    return LLM(
        provider="groq",
        model=MODEL_NAME,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,
    )


def _build_agents(llm: LLM) -> tuple[Agent, Agent, Agent, Agent]:
    common = {"llm": llm, "max_rpm": MAX_RPM, "verbose": False}
    coordinator = Agent(
        role="Banking Operations Manager",
        goal="Analyze the request, delegate to the right specialist, and synthesize a precise answer.",
        backstory="You coordinate account, transaction, and customer service operations.",
        allow_delegation=True,
        **common,
    )
    accounts = Agent(
        role="Account Details Specialist",
        goal="Answer balances, account types, and profile questions from the Accounts MCP tool.",
        backstory="You work only with account records and never invent account data.",
        tools=[accounts_tool], allow_delegation=False, **common,
    )
    transactions = Agent(
        role="Transaction and Statement Specialist",
        goal="Answer transaction history and spending questions from the Transactions MCP tool.",
        backstory="You explain credits, debits, and spending clearly.",
        tools=[transactions_tool], allow_delegation=False, **common,
    )
    services = Agent(
        role="Customer Service Specialist",
        goal="Handle address, cheque book, and KYC requests from the Services MCP tool.",
        backstory="You accurately review and record service requests.",
        tools=[services_tool], allow_delegation=False, **common,
    )
    return coordinator, accounts, transactions, services


def build_crew() -> Crew:
    coordinator, accounts, transactions, services = _build_agents(create_llm())
    tasks = [
        Task(description="Handle account-related parts of {user_prompt} using USER-1001 or an explicit account_id.", expected_output="Account facts or a no-match message.", agent=accounts),
        Task(description="Handle transaction-related parts of {user_prompt} using ACCT-1001 by default.", expected_output="Transaction facts or a no-match message.", agent=transactions),
        Task(description="Handle service-related parts of {user_prompt} using USER-1001. Create only account_opening, address_change, cheque_book, or kyc_update requests.", expected_output="Service status or creation confirmation.", agent=services),
    ]
    return Crew(
        agents=[accounts, transactions, services],
        tasks=tasks,
        manager_agent=coordinator,
        process=Process.hierarchical,
        max_rpm=MAX_RPM,
        verbose=False,
        memory=False,
    )


@retry(
    retry=retry_if_exception(_is_rate_limit_error),
    wait=wait_exponential(multiplier=1, min=2, max=15),
    stop=stop_after_attempt(4),
    reraise=True,
)
def run_banking_assistant(user_prompt: str) -> str:
    time.sleep(0.15)
    return str(build_crew().kickoff(inputs={"user_prompt": user_prompt}))
