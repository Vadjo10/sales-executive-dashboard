from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.extractors.fake_store_extractor import FakeStoreExtractor
from src.utils.exceptions import APIConnectionError, CircuitBreakerOpenError

MOCK_PRODUCTS = [
    {
        "id": 1,
        "title": "Product A",
        "price": 29.99,
        "description": "A product",
        "category": "electronics",
        "image": "https://example.com/img.png",
        "rating": {"rate": 4.5, "count": 100},
    }
]

MOCK_CATEGORIES_RAW = ["electronics", "jewelery"]

MOCK_USERS = [
    {
        "id": 1,
        "email": "test@test.com",
        "username": "testuser",
        "password": "secret",
        "name": {"firstname": "John", "lastname": "Doe"},
        "address": {
            "city": "New York",
            "street": "5th Ave",
            "number": 100,
            "zipcode": "10001",
            "geolocation": {"lat": "40.7128", "long": "-74.0060"},
        },
        "phone": "1-234-567-8900",
    }
]

MOCK_CARTS = [
    {
        "id": 1,
        "userId": 1,
        "date": "2024-01-15T10:00:00Z",
        "products": [{"productId": 1, "quantity": 2}],
    }
]


@pytest.fixture
def extractor() -> FakeStoreExtractor:
    mock_client = MagicMock()
    return FakeStoreExtractor(api_client=mock_client)


def test_extract_products(extractor: FakeStoreExtractor) -> None:
    extractor.api.get.return_value = MOCK_PRODUCTS
    result = extractor.extract_products()
    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["title"] == "Product A"
    extractor.api.get.assert_called_once_with("/products")


def test_extract_users(extractor: FakeStoreExtractor) -> None:
    extractor.api.get.return_value = MOCK_USERS
    result = extractor.extract_users()
    assert len(result) == 1
    assert result[0]["email"] == "test@test.com"
    extractor.api.get.assert_called_once_with("/users")


def test_extract_carts(extractor: FakeStoreExtractor) -> None:
    extractor.api.get.return_value = MOCK_CARTS
    result = extractor.extract_carts()
    assert len(result) == 1
    assert result[0]["userId"] == 1
    extractor.api.get.assert_called_once_with("/carts")


def test_extract_categories(extractor: FakeStoreExtractor) -> None:
    extractor.api.get.return_value = MOCK_CATEGORIES_RAW
    result = extractor.extract_categories()
    assert len(result) == 2
    assert result[0]["name"] == "electronics"
    extractor.api.get.assert_called_once_with("/products/categories")


def test_extract_all(extractor: FakeStoreExtractor) -> None:
    extractor.api.get.side_effect = [
        MOCK_PRODUCTS,
        MOCK_CATEGORIES_RAW,
        MOCK_USERS,
        MOCK_CARTS,
    ]
    result = extractor.extract_all()
    assert "products" in result
    assert "categories" in result
    assert "users" in result
    assert "carts" in result
    assert len(result["products"]) == 1
    assert len(result["users"]) == 1


def test_extract_rejects_invalid_records(extractor: FakeStoreExtractor) -> None:
    extractor.api.get.return_value = [{"id": 1}]
    result = extractor.extract_products()
    assert result == []


def test_extract_raises_on_api_error(extractor: FakeStoreExtractor) -> None:
    extractor.api.get.side_effect = APIConnectionError("API is down")
    with pytest.raises(APIConnectionError):
        extractor.extract_products()


def test_extract_unknown_entity(extractor: FakeStoreExtractor) -> None:
    with pytest.raises(ValueError, match="Unknown entity"):
        extractor.extract(entity="unknown")
