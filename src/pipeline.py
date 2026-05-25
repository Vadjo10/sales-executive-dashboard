from __future__ import annotations

from typing import Any

import pandas as pd

from src.extractors.fake_store_extractor import FakeStoreExtractor
from src.loaders.postgres_loader import PostgresLoader
from src.logger import logger
from src.transformers.data_cleaner import DataCleaner
from src.transformers.data_enricher import DataEnricher
from src.utils.exceptions import PipelineError
from src.utils.helpers import timer


class Pipeline:
    def __init__(
        self,
        extractor: FakeStoreExtractor | None = None,
        cleaner: DataCleaner | None = None,
        enricher: DataEnricher | None = None,
        loader: PostgresLoader | None = None,
    ) -> None:
        self.extractor = extractor or FakeStoreExtractor()
        self.cleaner = cleaner or DataCleaner()
        self.enricher = enricher or DataEnricher()
        self.loader = loader or PostgresLoader()

    @timer
    def run_extraction(self) -> dict[str, list[dict[str, Any]]]:
        logger.info("Starting extraction...")
        data = self.extractor.extract_all()
        logger.info(
            f"Extracted: {len(data['products'])} products, "
            f"{len(data['users'])} users, "
            f"{len(data['carts'])} carts"
        )
        return data

    @timer
    def run_transformation(
        self, raw_data: dict[str, list[dict[str, Any]]]
    ) -> dict[str, pd.DataFrame]:
        logger.info("Starting transformation...")
        return {
            entity: self.enricher.transform(self.cleaner.transform(data))
            for entity, data in raw_data.items()
        }

    @timer
    def run_load(self, transformed: dict[str, pd.DataFrame]) -> dict[str, int]:
        logger.info("Starting load...")
        results = {}
        for entity, df in transformed.items():
            table_name = f"stg_api_{entity}"
            rows = self.loader.load_dataframe(df, table_name)
            results[entity] = rows
        return results

    @timer
    def run(self) -> dict[str, Any]:
        try:
            raw = self.run_extraction()
            transformed = self.run_transformation(raw)
            results = self.run_load(transformed)
            logger.info(f"Pipeline completed: {results}")
            return {"status": "success", "rows_loaded": results}
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise PipelineError(str(e)) from e
