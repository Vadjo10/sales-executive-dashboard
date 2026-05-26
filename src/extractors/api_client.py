from __future__ import annotations

import time
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings
from src.logger import logger
from src.utils.exceptions import (
    APIConnectionError,
    APIRequestError,
    CircuitBreakerOpenError,
)


class CircuitBreakerState:
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time: float | None = None

    def record_success(self) -> None:
        if self.state == CircuitBreakerState.HALF_OPEN:
            logger.info("Circuit breaker: half-open → closed (success)")
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if (
            self.state == CircuitBreakerState.HALF_OPEN
            or self.failure_count >= self.failure_threshold
        ):
            logger.warning(
                f"Circuit breaker: {self.state} → OPEN "
                f"({self.failure_count} failures)"
            )
            self.state = CircuitBreakerState.OPEN

    def allow_request(self) -> bool:
        if self.state == CircuitBreakerState.CLOSED:
            return True
        if self.state == CircuitBreakerState.OPEN:
            if self.last_failure_time is not None:
                elapsed = time.time() - self.last_failure_time
                if elapsed >= self.recovery_timeout:
                    logger.info("Circuit breaker: OPEN → half-open (timeout)")
                    self.state = CircuitBreakerState.HALF_OPEN
                    return True
            return False
        return True


class APIClient:
    def __init__(self) -> None:
        self.base_url = settings.api.base_url
        self.timeout = settings.api.timeout
        self._client: httpx.Client | None = None
        self.circuit_breaker = CircuitBreaker()

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
        reraise=True,
    )
    def get(self, endpoint: str) -> list[dict[str, Any]]:
        if not self.circuit_breaker.allow_request():
            raise CircuitBreakerOpenError(
                f"Circuit breaker is OPEN for {endpoint}"
            )
        logger.info(f"GET {endpoint}")
        try:
            response = self.client.get(endpoint)
            response.raise_for_status()
            self.circuit_breaker.record_success()
            return response.json()
        except httpx.TimeoutException as e:
            self.circuit_breaker.record_failure()
            raise APIConnectionError(f"Timeout on {endpoint}") from e
        except httpx.HTTPStatusError as e:
            self.circuit_breaker.record_failure()
            raise APIRequestError(
                f"HTTP {e.response.status_code} on {endpoint}"
            ) from e
        except httpx.RequestError as e:
            self.circuit_breaker.record_failure()
            raise APIConnectionError(f"Connection failed on {endpoint}") from e

    def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None

    def __enter__(self) -> APIClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
