"""Mock MCP endpoints backed by the SQLite model."""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from crewai.tools import BaseTool
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from models.database import DB_PATH, create_database


def _is_rate_limit_error(error: BaseException) -> bool:
    text = str(error).lower()
    return "429" in text or "rate limit" in text or "too many requests" in text


@retry(
    retry=retry_if_exception(_is_rate_limit_error),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    stop=stop_after_attempt(4),
    reraise=True,
)
def _run_query(query: str, parameters: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    if not DB_PATH.exists():
        create_database()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in connection.execute(query, parameters).fetchall()]
    finally:
        connection.close()


def _json(rows: list[dict[str, Any]]) -> str:
    return json.dumps(rows, indent=2, default=str)


class AccountsMCPTool(BaseTool):
    name: str = "accounts_mcp"
    description: str = "Fetch balances, account types, and profiles for USER-1001 or an account_id."

    def _run(self, user_id: str = "USER-1001", account_id: str = "") -> str:
        if account_id:
            rows = _run_query("SELECT account_id, customer_name, account_type, balance, currency, branch, phone, email FROM accounts WHERE account_id = ?", (account_id,))
        else:
            rows = _run_query("SELECT account_id, customer_name, account_type, balance, currency, branch, phone, email FROM accounts WHERE user_id = ?", (user_id,))
        return _json(rows) if rows else "No matching accounts found."


class TransactionsMCPTool(BaseTool):
    name: str = "transactions_mcp"
    description: str = "Fetch transactions or spending analysis for account_id ACCT-1001."

    def _run(self, account_id: str = "ACCT-1001", category: str = "") -> str:
        if category:
            rows = _run_query("SELECT transaction_date, description, category, transaction_type, amount FROM transactions WHERE account_id = ? AND lower(category) = lower(?) ORDER BY transaction_date DESC", (account_id, category))
        else:
            rows = _run_query("SELECT transaction_date, description, category, transaction_type, amount FROM transactions WHERE account_id = ? ORDER BY transaction_date DESC", (account_id,))
        return _json(rows) if rows else "No matching transactions found."


class ServicesMCPTool(BaseTool):
    name: str = "services_mcp"
    description: str = "Review or create account_opening, address_change, cheque_book, or kyc_update requests for USER-1001."

    def _run(self, user_id: str = "USER-1001", request_type: str = "", details: str = "") -> str:
        supported_request_types = {"account_opening", "address_change", "cheque_book", "kyc_update"}
        if request_type and request_type not in supported_request_types:
            return "Unsupported request type. Use account_opening, address_change, cheque_book, or kyc_update."
        if request_type and details:
            connection = sqlite3.connect(DB_PATH)
            try:
                connection.execute("INSERT INTO service_requests (user_id, request_type, details, status, created_at) VALUES (?, ?, ?, 'open', date('now'))", (user_id, request_type, details))
                connection.commit()
            finally:
                connection.close()
            return json.dumps({"status": "created", "request_type": request_type, "details": details})
        rows = _run_query("SELECT request_id, request_type, details, status, created_at FROM service_requests WHERE user_id = ? ORDER BY request_id DESC", (user_id,))
        return _json(rows) if rows else "No service requests found."


accounts_tool = AccountsMCPTool()
transactions_tool = TransactionsMCPTool()
services_tool = ServicesMCPTool()
