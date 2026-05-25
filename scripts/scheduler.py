#!/usr/bin/env python3
from __future__ import annotations

from apscheduler.schedulers.blocking import BlockingScheduler

from src.logger import logger
from src.pipeline import Pipeline


def run_pipeline_job() -> None:
    logger.info("Scheduled pipeline execution started")
    pipeline = Pipeline()
    try:
        result = pipeline.run()
        logger.info(f"Scheduled pipeline completed: {result}")
    except Exception as e:
        logger.error(f"Scheduled pipeline failed: {e}")


def main() -> None:
    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_pipeline_job,
        "cron",
        hour=2,
        minute=0,
        id="daily_pipeline",
        name="Daily ETL Pipeline",
    )
    logger.info("Scheduler started. Pipeline will run daily at 02:00")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")


if __name__ == "__main__":
    main()
