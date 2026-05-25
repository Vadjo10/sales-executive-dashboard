from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.loaders.postgres_loader import PostgresLoader


@pytest.fixture
def loader() -> PostgresLoader:
    mock_db = MagicMock()
    return PostgresLoader(database=mock_db)


def test_load_dataframe_empty(loader: PostgresLoader) -> None:
    df = pd.DataFrame()
    result = loader.load_dataframe(df, "test_table")
    assert result == 0


def test_load_dataframe_success(loader: PostgresLoader) -> None:
    df = pd.DataFrame({"id": [1, 2], "name": ["A", "B"]})
    loader.db.engine = MagicMock()
    result = loader.load_dataframe(df, "test_table")
    assert result == 2


def test_execute_sql(loader: PostgresLoader) -> None:
    loader.execute_sql("SELECT 1")
    loader.db.execute.assert_called_once_with("SELECT 1")
