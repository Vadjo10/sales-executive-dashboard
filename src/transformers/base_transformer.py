from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, data: list[dict[str, Any]]) -> pd.DataFrame:
        ...

    def to_dataframe(self, data: list[dict[str, Any]]) -> pd.DataFrame:
        return pd.DataFrame(data)

    def validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        df = df.copy()
        df.columns = [col.lower() for col in df.columns]
        return df
