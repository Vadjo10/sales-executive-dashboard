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

    def load_all(
        self, dataframes: dict[str, pd.DataFrame], schema: str = "staging"
    ) -> dict[str, int]:
        results: dict[str, int] = {}
        connection = self.db.engine.connect()
        transaction = connection.begin()
        try:
            for entity, df in dataframes.items():
                table_name = f"stg_api_{entity}"
                if df.empty:
                    logger.warning(
                        f"No data to load into {schema}.{table_name}"
                    )
                    results[entity] = 0
                    continue
                rows = len(df)
                df.to_sql(
                    name=table_name,
                    con=connection,
                    schema=schema,
                    if_exists="replace",
                    index=False,
                    method="multi",
                )
                results[entity] = rows
                logger.info(f"Loaded {rows} rows into {schema}.{table_name}")
            transaction.commit()
            logger.info("Transaction committed successfully")
            return results
        except Exception as e:
            transaction.rollback()
            logger.error(f"Transaction rolled back: {e}")
            raise DatabaseOperationError(
                f"Failed to load all data, transaction rolled back: {e}"
            ) from e
        finally:
            connection.close()

    def execute_sql(self, sql: str) -> None:
        self.db.execute(sql)
        logger.info("SQL executed successfully")
