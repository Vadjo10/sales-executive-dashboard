from __future__ import annotations

from typing import Any

from src.extractors.api_client import APIClient
from src.extractors.base_extractor import BaseExtractor
from src.logger import logger


class FakeStoreExtractor(BaseExtractor):
    ENDPOINTS = {
        "products": "/products",
        "categories": "/products/categories",
        "users": "/users",
        "carts": "/carts",
    }

    def __init__(self, api_client: APIClient | None = None) -> None:
        self.api = api_client or APIClient()

    def extract_products(self) -> list[dict[str, Any]]:
        logger.info("Extracting products...")
        data = self.api.get(self.ENDPOINTS["products"])
        return self.validate_response(data)

    def extract_categories(self) -> list[dict[str, Any]]:
        logger.info("Extracting categories...")
        data = self.api.get(self.ENDPOINTS["categories"])
        return self.validate_response(data)

    def extract_users(self) -> list[dict[str, Any]]:
        logger.info("Extracting users...")
        data = self.api.get(self.ENDPOINTS["users"])
        return self.validate_response(data)

    def extract_carts(self) -> list[dict[str, Any]]:
        logger.info("Extracting carts...")
        data = self.api.get(self.ENDPOINTS["carts"])
        return self.validate_response(data)

    def extract_all(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "products": self.extract_products(),
            "categories": self.extract_categories(),
            "users": self.extract_users(),
            "carts": self.extract_carts(),
        }

    def extract(self, **kwargs: Any) -> list[dict[str, Any]]:
        entity = kwargs.get("entity", "products")
        methods = {
            "products": self.extract_products,
            "categories": self.extract_categories,
            "users": self.extract_users,
            "carts": self.extract_carts,
        }
        extractor = methods.get(entity)
        if extractor is None:
            raise ValueError(f"Unknown entity: {entity}")
        return extractor()
