"""Backward-compatible entry point for the database model."""

from models.database import DB_PATH, create_database


if __name__ == "__main__":
    print(f"Created demo database at {create_database()}")
