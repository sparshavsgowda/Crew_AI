"""Controller boundary between the Streamlit view and CrewAI service."""

from __future__ import annotations

import json

from services.crew_service import run_banking_assistant
from tools.mcp_tools import accounts_tool, services_tool, transactions_tool


class BankingController:
    """Handle user prompts without exposing orchestration details to the view."""

    @staticmethod
    def _local_account_answer() -> str:
        result = accounts_tool._run(user_id="USER-1001")
        if not result.startswith("["):
            return result
        accounts = json.loads(result)
        lines = ["Your account balances are:"]
        for account in accounts:
            lines.append(f"- {account['account_type']} ({account['account_id']}): {account['currency']} {account['balance']:,.2f}")
        return "\n".join(lines)

    @staticmethod
    def _local_transactions_answer() -> str:
        result = transactions_tool._run(account_id="ACCT-1001")
        if not result.startswith("["):
            return result
        transactions = json.loads(result)
        lines = ["Your recent transactions are:"]
        for transaction in transactions:
            sign = "+" if transaction["transaction_type"] == "credit" else "-"
            lines.append(f"- {transaction['transaction_date']}: {transaction['description']} ({sign}{transaction['amount']:,.2f})")
        return "\n".join(lines)

    @staticmethod
    def _local_services_answer() -> str:
        result = services_tool._run(user_id="USER-1001")
        if not result.startswith("["):
            return result
        requests = json.loads(result)
        lines = ["Your service requests are:"]
        for request in requests:
            lines.append(
                f"- {request['request_type']}: {request['status']} "
                f"({request['details']}, {request['created_at']})"
            )
        return "\n".join(lines)

    def answer(self, prompt: str) -> str:
        if not prompt.strip():
            return "Please enter a banking question."
        normalized_prompt = prompt.strip().lower()
        account_actions = ("create", "open")
        if "account" in normalized_prompt and any(action in normalized_prompt for action in account_actions):
            services_tool._run(
                user_id="USER-1001",
                request_type="account_opening",
                details="Customer requested a new bank account.",
            )
            return "Your account-opening request was created successfully. Our team will contact you with the next steps."
        if "balance" in normalized_prompt or "balances" in normalized_prompt:
            return self._local_account_answer()
        if "transaction" in normalized_prompt or "spending" in normalized_prompt:
            return self._local_transactions_answer()
        if any(word in normalized_prompt for word in ("service", "request", "address", "cheque", "kyc")):
            return self._local_services_answer()
        return run_banking_assistant(prompt.strip())
