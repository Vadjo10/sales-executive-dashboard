from __future__ import annotations

from typing import Any

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from src.config import settings
from src.logger import logger
from src.utils.exceptions import DatabaseConnectionError, DatabaseOperationError


class Database:
    def __init__(self, connection_string: str | None = None) -> None:
        self.connection_string = connection_string or settings.database.connection_string
        self._engine: Engine | None = None

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            try:
                self._engine = create_engine(self.connection_string)
                logger.info("Database engine created")
            except SQLAlchemyError as e:
                raise DatabaseConnectionError(str(e)) from e
        return self._engine

    def execute(self, sql: str, params: dict[str, Any] | None = None) -> Any:
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql), params or {})
                conn.commit()
                return result
        except SQLAlchemyError as e:
            raise DatabaseOperationError(str(e)) from e

    def test_connection(self) -> bool:
        try:
            self.execute("SELECT 1")
            logger.info("Database connection OK")
            return True
        except DatabaseConnectionError:
            logger.error("Database connection failed")
            return False

    def close(self) -> None:
        if self._engine:
            self._engine.dispose()
            self._engine = None
            logger.info("Database engine disposed")
