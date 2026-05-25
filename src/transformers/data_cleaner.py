from __future__ import annotations

import json
from typing import Any

import pandas as pd

from src.logger import logger
from src.transformers.base_transformer import BaseTransformer


class DataCleaner(BaseTransformer):
    def transform(self, data: list[dict[str, Any]]) -> pd.DataFrame:
        df = self.to_dataframe(data)
        df = self.validate_dataframe(df)
        df = self._serialize_nested(df)
        df = self._remove_duplicates(df)
        df = self._clean_strings(df)
        df = self._convert_types(df)
        return df

    def _serialize_nested(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
                df[col] = df[col].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x)
        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        if removed:
            logger.warning(f"Removed {removed} duplicate rows")
        return df

    def _clean_strings(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.select_dtypes(include="str").columns:
            df[col] = df[col].astype(str).str.strip().replace("nan", None)
        return df

    def _convert_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            if "price" in col or "total" in col or "amount" in col:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            if "quantity" in col or "id" in col:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        return df
