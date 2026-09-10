"""Backward-compatible exports for the CrewAI service."""

from services.crew_service import build_crew, create_llm, run_banking_assistant

__all__ = ["build_crew", "create_llm", "run_banking_assistant"]
