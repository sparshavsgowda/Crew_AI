"""Backward-compatible exports for the MVC MCP tools."""

from tools.mcp_tools import accounts_tool, services_tool, transactions_tool

__all__ = ["accounts_tool", "services_tool", "transactions_tool"]
