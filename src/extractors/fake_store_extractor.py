from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from src.extractors.api_client import APIClient
from src.extractors.base_extractor import BaseExtractor
from src.logger import logger
from src.models.schemas import (
    CartSchema,
    CategorySchema,
    ProductSchema,
    UserSchema,
    ValidationReport,
)
from src.utils.exceptions import DataRejectedError


ENTITY_SCHEMAS = {
    "products": ProductSchema,
    "categories": CategorySchema,
    "users": UserSchema,
    "carts": CartSchema,
}


class FakeStoreExtractor(BaseExtractor):
    ENDPOINTS = {
        "products": "/products",
        "categories": "/products/categories",
        "users": "/users",
        "carts": "/carts",
    }

    def __init__(self, api_client: APIClient | None = None) -> None:
        self.api = api_client or APIClient()

    def _validate_records(
        self, entity: str, records: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        schema_cls = ENTITY_SCHEMAS.get(entity)
        if schema_cls is None:
            return records

        valid: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []

        for i, record in enumerate(records):
            try:
                validated = schema_cls.model_validate(record)
                valid.append(validated.model_dump())
            except ValidationError as e:
                error_detail = {
                    "index": i,
                    "record_id": record.get("id"),
                    "errors": e.errors(),
                }
                errors.append(error_detail)
                logger.warning(
                    f"Rejected {entity}[{i}] (id={record.get('id')}): {e.errors()}"
                )

        report = ValidationReport(
            entity=entity,
            total=len(records),
            valid=len(valid),
            rejected=len(errors),
            errors=errors,
        )

        if errors:
            logger.warning(
                f"{entity}: {report.rejected}/{report.total} records rejected"
            )

        return valid

    def extract_products(self) -> list[dict[str, Any]]:
        logger.info("Extracting products...")
        data = self.api.get(self.ENDPOINTS["products"])
        data = self.validate_response(data)
        return self._validate_records("products", data)

    def extract_categories(self) -> list[dict[str, Any]]:
        logger.info("Extracting categories...")
        data = self.api.get(self.ENDPOINTS["categories"])
        data = self.validate_response(data)
        formatted = [{"name": c} if isinstance(c, str) else c for c in data]
        return self._validate_records("categories", formatted)

    def extract_users(self) -> list[dict[str, Any]]:
        logger.info("Extracting users...")
        data = self.api.get(self.ENDPOINTS["users"])
        data = self.validate_response(data)
        return self._validate_records("users", data)

    def extract_carts(self) -> list[dict[str, Any]]:
        logger.info("Extracting carts...")
        data = self.api.get(self.ENDPOINTS["carts"])
        data = self.validate_response(data)
        return self._validate_records("carts", data)

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
