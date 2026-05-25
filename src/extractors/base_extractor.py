from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from src.logger import logger


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, **kwargs: Any) -> list[dict[str, Any]]:
        ...

    def validate_response(self, data: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
        if data is None:
            logger.warning("Received None response from API")
            return []
        if not isinstance(data, list):
            logger.warning(f"Unexpected response type: {type(data)}")
            return []
        logger.info(f"Validated {len(data)} records")
        return data
