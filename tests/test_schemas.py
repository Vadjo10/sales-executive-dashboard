from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.models.schemas import (
    CartSchema,
    CategorySchema,
    ProductSchema,
    RatingSchema,
    UserSchema,
)


class TestProductSchema:
    def test_valid_product(self) -> None:
        data = {
            "id": 1,
            "title": "Test Product",
            "price": 29.99,
            "description": "A test product",
            "category": "electronics",
            "image": "https://example.com/img.png",
            "rating": {"rate": 4.5, "count": 100},
        }
        product = ProductSchema.model_validate(data)
        assert product.id == 1
        assert product.price == 29.99

    def test_missing_required_fields(self) -> None:
        with pytest.raises(ValidationError) as exc:
            ProductSchema.model_validate({"id": 1})
        errors = {e["loc"][0] for e in exc.value.errors()}
        assert "title" in errors
        assert "price" in errors
        assert "description" in errors
        assert "category" in errors

    def test_negative_price(self) -> None:
        with pytest.raises(ValidationError):
            ProductSchema.model_validate(
                {
                    "id": 1,
                    "title": "Test",
                    "price": -10,
                    "description": "desc",
                    "category": "cat",
                }
            )

    def test_image_optional(self) -> None:
        data = {
            "id": 1,
            "title": "Test",
            "price": 10.0,
            "description": "desc",
            "category": "cat",
        }
        product = ProductSchema.model_validate(data)
        assert product.image is None


class TestUserSchema:
    def test_valid_user(self) -> None:
        data = {
            "id": 1,
            "email": "user@test.com",
            "username": "testuser",
            "password": "secret123",
            "name": {"firstname": "John", "lastname": "Doe"},
            "address": {
                "city": "NYC",
                "street": "5th Ave",
                "number": 100,
                "zipcode": "10001",
                "geolocation": {"lat": "40.7", "long": "-74.0"},
            },
            "phone": "123-456-7890",
        }
        user = UserSchema.model_validate(data)
        assert user.email == "user@test.com"
        assert user.name is not None
        assert user.name.firstname == "John"

    def test_invalid_email(self) -> None:
        with pytest.raises(ValidationError):
            UserSchema.model_validate(
                {"id": 1, "email": "invalid", "username": "test"}
            )

    def test_minimal_user(self) -> None:
        data = {"id": 1, "email": "a@b.com", "username": "test"}
        user = UserSchema.model_validate(data)
        assert user.id == 1
        assert user.name is None


class TestCartSchema:
    def test_valid_cart(self) -> None:
        data = {
            "id": 1,
            "userId": 1,
            "date": "2024-01-15T10:00:00Z",
            "products": [{"productId": 1, "quantity": 2}],
        }
        cart = CartSchema.model_validate(data)
        assert cart.id == 1
        assert len(cart.products) == 1

    def test_missing_date(self) -> None:
        with pytest.raises(ValidationError):
            CartSchema.model_validate({"id": 1, "userId": 1})

    def test_empty_products(self) -> None:
        data = {
            "id": 1,
            "userId": 1,
            "date": "2024-01-15T10:00:00Z",
            "products": [],
        }
        cart = CartSchema.model_validate(data)
        assert cart.products == []

    def test_zero_quantity(self) -> None:
        with pytest.raises(ValidationError):
            CartSchema.model_validate(
                {
                    "id": 1,
                    "userId": 1,
                    "date": "2024-01-15T10:00:00Z",
                    "products": [{"productId": 1, "quantity": 0}],
                }
            )


class TestCategorySchema:
    def test_valid_category(self) -> None:
        cat = CategorySchema.model_validate({"name": "electronics"})
        assert cat.name == "electronics"


class TestRatingSchema:
    def test_valid_rating(self) -> None:
        r = RatingSchema.model_validate({"rate": 4.5, "count": 100})
        assert r.rate == 4.5

    def test_rate_out_of_range(self) -> None:
        with pytest.raises(ValidationError):
            RatingSchema.model_validate({"rate": 6, "count": 1})
