from __future__ import annotations

from typing import Any

import pandas as pd
from sqlalchemy import Engine

from src.logger import logger
from src.loaders.database import Database
from src.utils.exceptions import DatabaseOperationError


class PostgresLoader:
    def __init__(self, database: Database | None = None) -> None:
        self.db = database or Database()

    def load_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema: str = "staging",
        if_exists: str = "replace",
    ) -> int:
        if df.empty:
            logger.warning(f"No data to load into {schema}.{table_name}")
            return 0

        try:
            rows = len(df)
            df.to_sql(
                name=table_name,
                con=self.db.engine,
                schema=schema,
                if_exists=if_exists,
                index=False,
                method="multi",
            )
            logger.info(f"Loaded {rows} rows into {schema}.{table_name}")
            return rows
        except Exception as e:
            raise DatabaseOperationError(
                f"Failed to load data into {schema}.{table_name}: {e}"
            ) from e

    def execute_sql(self, sql: str) -> None:
        self.db.execute(sql)
        logger.info("SQL executed successfully")
