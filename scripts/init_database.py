#!/usr/bin/env python3
from __future__ import annotations

from src.loaders.database import Database
from src.logger import logger
from src.models.staging import Base as StagingBase
from src.models.warehouse import Base as WarehouseBase


def create_schemas(db: Database) -> None:
    logger.info("Creating schemas...")
    db.execute("CREATE SCHEMA IF NOT EXISTS staging")
    db.execute("CREATE SCHEMA IF NOT EXISTS warehouse")
    logger.info("Schemas created successfully")


def create_tables(db: Database) -> None:
    logger.info("Creating staging tables...")
    StagingBase.metadata.create_all(db.engine)

    logger.info("Creating warehouse tables...")
    WarehouseBase.metadata.create_all(db.engine)

    logger.info("All tables created successfully")


def populate_dim_date(db: Database) -> None:
    logger.info("Populating dim_dates...")
    db.execute("""
        INSERT INTO warehouse.dim_dates (date_id, date, year, month, quarter, day_of_week, week_of_year)
        SELECT
            d::date,
            d::date,
            EXTRACT(YEAR FROM d)::int,
            EXTRACT(MONTH FROM d)::int,
            EXTRACT(QUARTER FROM d)::int,
            EXTRACT(DOW FROM d)::int,
            EXTRACT(WEEK FROM d)::int
        FROM generate_series('2023-01-01'::date, '2026-12-31'::date, '1 day'::interval) AS d
        ON CONFLICT (date_id) DO NOTHING
    """)
    logger.info("dim_dates populated")


def main() -> None:
    db = Database()
    if not db.test_connection():
        logger.error("Cannot connect to database. Aborting.")
        return

    create_schemas(db)
    create_tables(db)
    populate_dim_date(db)
    db.close()
    logger.info("Database initialization completed successfully")


if __name__ == "__main__":
    main()
