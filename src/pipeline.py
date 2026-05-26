from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import settings
from src.extractors.fake_store_extractor import FakeStoreExtractor
from src.loaders.postgres_loader import PostgresLoader
from src.logger import logger
from src.transformers.data_cleaner import DataCleaner
from src.transformers.data_enricher import DataEnricher
from src.utils.exceptions import PipelineError
from src.utils.helpers import timer


CHECKPOINT_DIR = settings.root_dir / "checkpoints"


class Pipeline:
    def __init__(
        self,
        extractor: FakeStoreExtractor | None = None,
        cleaner: DataCleaner | None = None,
        enricher: DataEnricher | None = None,
        loader: PostgresLoader | None = None,
        checkpoint: bool = True,
    ) -> None:
        self.extractor = extractor or FakeStoreExtractor()
        self.cleaner = cleaner or DataCleaner()
        self.enricher = enricher or DataEnricher()
        self.loader = loader or PostgresLoader()
        self.checkpoint = checkpoint

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

    def _save_checkpoint(
        self, transformed: dict[str, pd.DataFrame], run_id: str
    ) -> None:
        checkpoint_dir = CHECKPOINT_DIR / run_id
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        for entity, df in transformed.items():
            path = checkpoint_dir / f"{entity}.parquet"
            df.to_parquet(path, index=False)
            logger.info(f"Checkpoint saved: {path}")

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
        run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        try:
            raw = self.run_extraction()
            transformed = self.run_transformation(raw)
            if self.checkpoint:
                self._save_checkpoint(transformed, run_id)
            results = self.loader.load_all(transformed)
            logger.info(f"Pipeline completed: {results}")
            return {"status": "success", "rows_loaded": results, "run_id": run_id}
        except Exception as e:
            logger.error(f"Pipeline failed at {run_id}: {e}")
            raise PipelineError(str(e)) from e
