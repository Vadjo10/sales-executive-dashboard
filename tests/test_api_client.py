from __future__ import annotations

from unittest.mock import patch

import httpx
import pytest
import respx

from src.config import settings
from src.extractors.api_client import APIClient, CircuitBreaker
from src.utils.exceptions import (
    APIConnectionError,
    APIRequestError,
    CircuitBreakerOpenError,
)


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def breaker() -> CircuitBreaker:
    return CircuitBreaker(failure_threshold=2, recovery_timeout=60.0)


def test_circuit_breaker_starts_closed(breaker: CircuitBreaker) -> None:
    assert breaker.allow_request() is True
    assert breaker.state == "CLOSED"


def test_circuit_breaker_opens_after_threshold(breaker: CircuitBreaker) -> None:
    breaker.record_failure()
    assert breaker.allow_request() is True
    breaker.record_failure()
    assert breaker.allow_request() is False
    assert breaker.state == "OPEN"


def test_circuit_breaker_half_open_recovers(breaker: CircuitBreaker) -> None:
    breaker.record_failure()
    breaker.record_failure()
    assert breaker.state == "OPEN"
    breaker.last_failure_time = 0
    assert breaker.allow_request() is True
    assert breaker.state == "HALF_OPEN"
    breaker.record_success()
    assert breaker.state == "CLOSED"


def test_circuit_breaker_half_open_fails_again(breaker: CircuitBreaker) -> None:
    breaker.record_failure()
    breaker.record_failure()
    breaker.last_failure_time = 0
    breaker.allow_request()
    assert breaker.state == "HALF_OPEN"
    breaker.record_failure()
    assert breaker.state == "OPEN"


@respx.mock
def test_api_client_get_success(client: APIClient) -> None:
    route = respx.get(f"{settings.api.base_url}/products").respond(
        json=[{"id": 1, "title": "Test"}]
    )
    result = client.get("/products")
    assert result == [{"id": 1, "title": "Test"}]
    assert route.called


@respx.mock
def test_api_client_get_timeout(client: APIClient) -> None:
    respx.get(f"{settings.api.base_url}/products").mock(
        side_effect=httpx.TimeoutException("timeout")
    )
    with pytest.raises(APIConnectionError, match="Timeout"):
        client.get("/products")


@respx.mock
def test_api_client_get_http_error(client: APIClient) -> None:
    respx.get(f"{settings.api.base_url}/products").respond(status_code=500)
    with pytest.raises(APIRequestError, match="HTTP 500"):
        client.get("/products")


@respx.mock
def test_api_client_circuit_breaker_blocks(client: APIClient) -> None:
    client.circuit_breaker.state = "OPEN"
    with pytest.raises(CircuitBreakerOpenError):
        client.get("/products")
