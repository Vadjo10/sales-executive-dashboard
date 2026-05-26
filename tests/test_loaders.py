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


def test_load_all_success(loader: PostgresLoader) -> None:
    mock_conn = MagicMock()
    mock_transaction = MagicMock()
    mock_conn.begin.return_value = mock_transaction
    loader.db.engine.connect.return_value = mock_conn

    with patch("pandas.DataFrame.to_sql") as mock_to_sql:
        dataframes = {
            "products": pd.DataFrame({"id": [1, 2]}),
            "users": pd.DataFrame({"id": [3]}),
        }
        results = loader.load_all(dataframes)
    assert results["products"] == 2
    assert results["users"] == 1
    mock_transaction.commit.assert_called_once()


def test_load_all_empty_dataframe(loader: PostgresLoader) -> None:
    mock_conn = MagicMock()
    mock_transaction = MagicMock()
    mock_conn.begin.return_value = mock_transaction
    loader.db.engine.connect.return_value = mock_conn

    dataframes = {
        "products": pd.DataFrame(),
        "users": pd.DataFrame({"id": [1]}),
    }
    results = loader.load_all(dataframes)
    assert results["products"] == 0
    assert results["users"] == 1


def test_load_all_rollback_on_failure(loader: PostgresLoader) -> None:
    mock_conn = MagicMock()
    mock_transaction = MagicMock()
    mock_conn.begin.return_value = mock_transaction
    loader.db.engine.connect.return_value = mock_conn

    with patch("pandas.DataFrame.to_sql", side_effect=Exception("DB Error")):
        from src.utils.exceptions import DatabaseOperationError

        with pytest.raises(DatabaseOperationError):
            loader.load_all({"products": pd.DataFrame({"id": [1]})})
    mock_transaction.rollback.assert_called_once()
