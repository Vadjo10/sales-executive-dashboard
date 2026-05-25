from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.extractors.fake_store_extractor import FakeStoreExtractor
from src.utils.exceptions import APIConnectionError


@pytest.fixture
def extractor() -> FakeStoreExtractor:
    mock_client = MagicMock()
    return FakeStoreExtractor(api_client=mock_client)


def test_extract_products(extractor: FakeStoreExtractor) -> None:
    mock_data = [{"id": 1, "title": "Product A"}]
    extractor.api.get.return_value = mock_data

    result = extractor.extract_products()
    assert result == mock_data
    extractor.api.get.assert_called_once_with("/products")


def test_extract_users(extractor: FakeStoreExtractor) -> None:
    mock_data = [{"id": 1, "email": "test@test.com"}]
    extractor.api.get.return_value = mock_data

    result = extractor.extract_users()
    assert result == mock_data
    extractor.api.get.assert_called_once_with("/users")


def test_extract_carts(extractor: FakeStoreExtractor) -> None:
    mock_data = [{"id": 1, "userId": 1}]
    extractor.api.get.return_value = mock_data

    result = extractor.extract_carts()
    assert result == mock_data
    extractor.api.get.assert_called_once_with("/carts")


def test_extract_categories(extractor: FakeStoreExtractor) -> None:
    mock_data = ["electronics", "jewelery"]
    extractor.api.get.return_value = mock_data

    result = extractor.extract_categories()
    assert result == mock_data
    extractor.api.get.assert_called_once_with("/products/categories")


def test_extract_all(extractor: FakeStoreExtractor) -> None:
    extractor.api.get.side_effect = [
        [{"id": 1}],
        ["cat1"],
        [{"id": 1}],
        [{"id": 1}],
    ]

    result = extractor.extract_all()
    assert "products" in result
    assert "categories" in result
    assert "users" in result
    assert "carts" in result


def test_extract_raises_on_api_error(extractor: FakeStoreExtractor) -> None:
    extractor.api.get.side_effect = APIConnectionError("API is down")

    with pytest.raises(APIConnectionError):
        extractor.extract_products()


def test_extract_unknown_entity(extractor: FakeStoreExtractor) -> None:
    with pytest.raises(ValueError, match="Unknown entity"):
        extractor.extract(entity="unknown")
