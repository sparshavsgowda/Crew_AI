"""SQLite persistence model and demo data generator."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "bank_data.db"


def create_database(db_path: str | Path = DB_PATH) -> Path:
    """Create and seed the local demo database."""
    db_path = Path(db_path)
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(
            """
            DROP TABLE IF EXISTS accounts;
            DROP TABLE IF EXISTS transactions;
            DROP TABLE IF EXISTS service_requests;

            CREATE TABLE accounts (
                account_id TEXT PRIMARY KEY, user_id TEXT NOT NULL,
                customer_name TEXT NOT NULL, account_type TEXT NOT NULL,
                balance REAL NOT NULL, currency TEXT NOT NULL,
                branch TEXT NOT NULL, phone TEXT NOT NULL, email TEXT NOT NULL
            );
            CREATE TABLE transactions (
                transaction_id TEXT PRIMARY KEY, account_id TEXT NOT NULL,
                transaction_date TEXT NOT NULL, description TEXT NOT NULL,
                category TEXT NOT NULL, transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id)
            );
            CREATE TABLE service_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL,
                request_type TEXT NOT NULL, details TEXT NOT NULL,
                status TEXT NOT NULL, created_at TEXT NOT NULL
            );
            """
        )
        connection.executemany(
            "INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("ACCT-1001", "USER-1001", "Avery Morgan", "Checking", 4280.75, "USD", "Downtown", "+1-555-0101", "avery@example.test"),
                ("ACCT-1002", "USER-1001", "Avery Morgan", "Savings", 12650.40, "USD", "Downtown", "+1-555-0101", "avery@example.test"),
                ("ACCT-2001", "USER-2001", "Jordan Lee", "Checking", 1890.22, "USD", "Riverside", "+1-555-0102", "jordan@example.test"),
                ("ACCT-3001", "USER-3001", "Sam Taylor", "Checking", 7635.10, "USD", "Market Street", "+1-555-0103", "sam@example.test"),
                ("ACCT-4001", "USER-4001", "Priya Shah", "Savings", 22100.00, "USD", "Lakeside", "+1-555-0104", "priya@example.test"),
            ],
        )
        connection.executemany(
            "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                ("TX-0001", "ACCT-1001", "2026-08-29", "Grocery Market", "Groceries", "debit", 86.42),
                ("TX-0002", "ACCT-1001", "2026-09-01", "Salary Deposit", "Income", "credit", 3200.00),
                ("TX-0003", "ACCT-1001", "2026-09-03", "Electric Utility", "Bills", "debit", 142.18),
                ("TX-0004", "ACCT-1001", "2026-09-05", "Metro Transit", "Transport", "debit", 42.50),
                ("TX-0005", "ACCT-1002", "2026-08-15", "Interest Credit", "Interest", "credit", 18.77),
                ("TX-0006", "ACCT-1002", "2026-08-20", "Transfer from Checking", "Transfer", "credit", 500.00),
                ("TX-0007", "ACCT-2001", "2026-09-02", "Pharmacy", "Healthcare", "debit", 35.90),
                ("TX-0008", "ACCT-3001", "2026-09-04", "Online Retail", "Shopping", "debit", 129.99),
            ],
        )
        connection.executemany(
            "INSERT INTO service_requests (user_id, request_type, details, status, created_at) VALUES (?, ?, ?, ?, ?)",
            [
                ("USER-1001", "address_change", "Update mailing address to 18 Cedar Lane", "open", "2026-09-01"),
                ("USER-1001", "cheque_book", "25-leaf cheque book for checking account", "completed", "2026-08-20"),
                ("USER-2001", "kyc_update", "Occupation and identification document refresh", "pending", "2026-09-03"),
                ("USER-3001", "address_change", "Update residential address", "open", "2026-09-05"),
                ("USER-4001", "cheque_book", "50-leaf cheque book", "completed", "2026-08-28"),
            ],
        )
        connection.commit()
    finally:
        connection.close()
    return db_path


if __name__ == "__main__":
    print(f"Created demo database at {create_database()}")
