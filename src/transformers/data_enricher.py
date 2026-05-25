from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.transformers.base_transformer import BaseTransformer


class DataEnricher(BaseTransformer):
    def transform(self, data: list[dict[str, Any]]) -> pd.DataFrame:
        df = self.to_dataframe(data)
        df = self.validate_dataframe(df)
        df = self._add_processing_metadata(df)
        return df

    def _add_processing_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        df["processed_at"] = datetime.now(timezone.utc).isoformat()
        return df
