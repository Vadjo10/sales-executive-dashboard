from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings
from src.logger import logger
from src.utils.exceptions import APIConnectionError, APIRequestError


class APIClient:
    def __init__(self) -> None:
        self.base_url = settings.api.base_url
        self.timeout = settings.api.timeout
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=self.timeout,
            )
        return self._client

    @retry(
        stop=stop_after_attempt(settings.api.max_retries),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    def get(self, endpoint: str) -> list[dict[str, Any]]:
        logger.info(f"GET {endpoint}")
        try:
            response = self.client.get(endpoint)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as e:
            raise APIConnectionError(f"Timeout on {endpoint}") from e
        except httpx.HTTPStatusError as e:
            raise APIRequestError(f"HTTP {e.response.status_code} on {endpoint}") from e
        except httpx.RequestError as e:
            raise APIConnectionError(f"Connection failed on {endpoint}") from e

    def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None

    def __enter__(self) -> APIClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
