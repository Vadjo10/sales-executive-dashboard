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


class TestDataCleaner:
    def test_removes_duplicates(self, cleaner: DataCleaner) -> None:
        data = [{"id": 1, "name": "A"}, {"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
        df = cleaner.transform(data)
        assert len(df) == 2

    def test_converts_types(self, cleaner: DataCleaner) -> None:
        data = [{"id": "1", "price": "29.99", "quantity": "5"}]
        df = cleaner.transform(data)
        assert df["price"].dtype == "float64"
        assert df["quantity"].dtype == "Int64"

    def test_handles_empty(self, cleaner: DataCleaner) -> None:
        df = cleaner.transform([])
        assert df.empty

    def test_serializes_nested_dicts(self, cleaner: DataCleaner) -> None:
        data = [{"id": 1, "nested": {"key": "value"}}]
        df = cleaner.transform(data)
        assert isinstance(df["nested"].iloc[0], str)

    def test_serializes_nested_lists(self, cleaner: DataCleaner) -> None:
        data = [{"id": 1, "items": [1, 2, 3]}]
        df = cleaner.transform(data)
        assert isinstance(df["items"].iloc[0], str)

    def test_cleans_string_whitespace(self, cleaner: DataCleaner) -> None:
        data = [{"id": 1, "name": "  hello  "}]
        df = cleaner.transform(data)
        assert df["name"].iloc[0] == "hello"


class TestDataEnricher:
    def test_adds_timestamp(self, enricher: DataEnricher) -> None:
        data = [{"id": 1, "name": "Test"}]
        df = enricher.transform(data)
        assert "processed_at" in df.columns
        assert df["processed_at"].iloc[0] is not None

    def test_handles_empty(self, enricher: DataEnricher) -> None:
        df = enricher.transform([])
        assert df.empty

    def test_adds_has_nulls_flag(self, enricher: DataEnricher) -> None:
        data = [{"id": 1, "name": None}]
        df = enricher.transform(data)
        assert "has_nulls" in df.columns
        assert bool(df["has_nulls"].iloc[0]) is True

    def test_no_nulls_flag_false(self, enricher: DataEnricher) -> None:
        data = [{"id": 1, "name": "Test"}]
        df = enricher.transform(data)
        assert bool(df["has_nulls"].iloc[0]) is False

    def test_quantity_aggregation(self, enricher: DataEnricher) -> None:
        data = [{"id": 1, "quantity": 5}, {"id": 2, "quantity": 15}]
        df = enricher.transform(data)
        assert "quantity_bucket" in df.columns
        assert df["quantity_bucket"].iloc[0] == "below_avg"
        assert df["quantity_bucket"].iloc[1] == "above_avg"

    def test_price_aggregation(self, enricher: DataEnricher) -> None:
        data = [{"id": 1, "price": 10}, {"id": 2, "price": 100}]
        df = enricher.transform(data)
        assert "price_bucket" in df.columns
