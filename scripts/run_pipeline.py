#!/usr/bin/env python3
from __future__ import annotations

from src.logger import logger
from src.pipeline import Pipeline


def main() -> None:
    logger.info("Starting ETL pipeline...")
    pipeline = Pipeline()
    result = pipeline.run()

    if result["status"] == "success":
        logger.info(f"Pipeline finished. Rows loaded: {result['rows_loaded']}")
    else:
        logger.error("Pipeline failed")
        exit(1)


if __name__ == "__main__":
    main()
