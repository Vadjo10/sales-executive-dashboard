from __future__ import annotations

import pandas as pd
import pytest

from src.transformers.data_cleaner import DataCleaner
from src.transformers.data_enricher import DataEnricher


@pytest.fixture
def cleaner() -> DataCleaner:
    return DataCleaner()


@pytest.fixture
def enricher() -> DataEnricher:
    return DataEnricher()


def test_cleaner_removes_duplicates(cleaner: DataCleaner) -> None:
    data = [{"id": 1, "name": "A"}, {"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
    df = cleaner.transform(data)
    assert len(df) == 2


def test_cleaner_converts_types(cleaner: DataCleaner) -> None:
    data = [{"id": "1", "price": "29.99", "quantity": "5"}]
    df = cleaner.transform(data)
    assert df["price"].dtype == "float64"
    assert df["quantity"].dtype == "Int64"


def test_cleaner_handles_empty(cleaner: DataCleaner) -> None:
    df = cleaner.transform([])
    assert df.empty


def test_enricher_adds_timestamp(enricher: DataEnricher) -> None:
    data = [{"id": 1, "name": "Test"}]
    df = enricher.transform(data)
    assert "processed_at" in df.columns
    assert df["processed_at"].iloc[0] is not None


def test_enricher_handles_empty(enricher: DataEnricher) -> None:
    df = enricher.transform([])
    assert df.empty
