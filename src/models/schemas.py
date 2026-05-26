from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class RatingSchema(BaseModel):
    rate: float = Field(ge=0, le=5)
    count: int = Field(ge=0)


class ProductSchema(BaseModel):
    id: int
    title: str
    price: float = Field(ge=0)
    description: str
    category: str
    image: str | None = None
    rating: RatingSchema | None = None


class GeolocationSchema(BaseModel):
    lat: str | None = None
    long: str | None = None


class NameSchema(BaseModel):
    firstname: str
    lastname: str


class AddressSchema(BaseModel):
    city: str
    street: str
    number: int | str | None = None
    zipcode: str | None = None
    geolocation: GeolocationSchema | None = None


class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    password: str | None = None
    name: NameSchema | None = None
    address: AddressSchema | None = None
    phone: str | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email")
        return v


class CartProductSchema(BaseModel):
    productId: int
    quantity: int = Field(gt=0)


class CartSchema(BaseModel):
    id: int
    userId: int
    date: datetime | str
    products: list[CartProductSchema] = []

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v: str | datetime) -> datetime:
        if isinstance(v, datetime):
            return v
        try:
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return v


class CategorySchema(BaseModel):
    name: str


class ValidationReport(BaseModel):
    entity: str
    total: int
    valid: int
    rejected: int
    errors: list[dict[str, Any]] = []
