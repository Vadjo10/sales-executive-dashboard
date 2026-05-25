from __future__ import annotations

from typing import Any

import pytest


@pytest.fixture
def sample_product() -> dict[str, Any]:
    return {
        "id": 1,
        "title": "Test Product",
        "price": 29.99,
        "description": "A test product",
        "category": "electronics",
        "image": "https://example.com/img.png",
        "rating": {"rate": 4.5, "count": 100},
    }


@pytest.fixture
def sample_user() -> dict[str, Any]:
    return {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "password": "secure123",
        "phone": "1-234-567-8900",
        "name": {"firstname": "John", "lastname": "Doe"},
        "address": {
            "city": "New York",
            "street": "123 Main St",
            "number": 42,
            "zipcode": "10001",
            "geolocation": {"lat": "40.7128", "long": "-74.0060"},
        },
    }


@pytest.fixture
def sample_cart() -> dict[str, Any]:
    return {
        "id": 1,
        "userId": 1,
        "date": "2024-01-01T00:00:00.000Z",
        "products": [{"productId": 1, "quantity": 2}],
    }


@pytest.fixture
def sample_products_list(sample_product: dict[str, Any]) -> list[dict[str, Any]]:
    return [sample_product]


@pytest.fixture
def sample_users_list(sample_user: dict[str, Any]) -> list[dict[str, Any]]:
    return [sample_user]


@pytest.fixture
def sample_carts_list(sample_cart: dict[str, Any]) -> list[dict[str, Any]]:
    return [sample_cart]
