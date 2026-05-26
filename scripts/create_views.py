#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from src.loaders.database import Database
from src.logger import logger


SQL_DIR = Path(__file__).resolve().parent


def deploy_views(db: Database) -> None:
    sql_path = SQL_DIR / "create_views.sql"
    if not sql_path.exists():
        logger.error(f"SQL file not found: {sql_path}")
        return

    sql = sql_path.read_text(encoding="utf-8")
    statements = [s.strip() for s in sql.split(";") if s.strip()]

    for stmt in statements:
        try:
            db.execute(stmt + ";")
            first_line = stmt.strip().split("\n")[0][:80]
            logger.info(f"Executed: {first_line}...")
        except Exception as e:
            logger.error(f"Failed to execute statement: {e}")
            raise

    logger.info("All views deployed successfully")


def main() -> None:
    db = Database()
    if not db.test_connection():
        logger.error("Cannot connect to database. Aborting.")
        return

    deploy_views(db)
    db.close()


if __name__ == "__main__":
    main()
