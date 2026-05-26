from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.logger import logger
from src.transformers.base_transformer import BaseTransformer


class DataEnricher(BaseTransformer):
    def transform(self, data: list[dict[str, Any]]) -> pd.DataFrame:
        df = self.to_dataframe(data)
        df = self.validate_dataframe(df)
        df = self._add_processing_metadata(df)
        df = self._add_quality_flags(df)
        df = self._compute_aggregations(df)
        return df

    def _add_processing_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        df["processed_at"] = datetime.now(timezone.utc).isoformat()
        return df

    def _add_quality_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        null_counts = df.isnull().sum()
        for col in df.columns:
            nulls = int(null_counts.get(col, 0))
            if nulls > 0:
                logger.warning(f"Quality: {col} has {nulls} null values")

        df["has_nulls"] = df.isnull().any(axis=1)
        return df

    def _compute_aggregations(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        quant_cols = ["quantity", "price", "total", "amount"]
        for col in quant_cols:
            if col in df.columns:
                agg_key = f"{col}_bucket"
                mean_val = df[col].mean()
                if mean_val is not None:
                    df[agg_key] = pd.cut(
                        df[col],
                        bins=[0, mean_val, float("inf")],
                        labels=["below_avg", "above_avg"],
                        right=False,
                    )
        return df
