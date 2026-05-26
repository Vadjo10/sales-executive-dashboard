from __future__ import annotations

import pytest

from src.utils.helpers import chunk_list, timer
from src.utils.validators import (
    validate_email,
    validate_non_empty,
    validate_phone,
    validate_price,
    validate_quantity,
)


class TestHelpers:
    def test_chunk_list(self) -> None:
        items = [1, 2, 3, 4, 5]
        chunks = chunk_list(items, 2)
        assert chunks == [[1, 2], [3, 4], [5]]

    def test_chunk_list_empty(self) -> None:
        assert chunk_list([], 3) == []

    def test_chunk_list_larger_than_list(self) -> None:
        assert chunk_list([1], 10) == [[1]]


class TestValidators:
    def test_validate_email_valid(self) -> None:
        assert validate_email("user@example.com") is True

    def test_validate_email_invalid(self) -> None:
        assert validate_email("not-an-email") is False

    def test_validate_phone_valid(self) -> None:
        assert validate_phone("123-456-7890") is True

    def test_validate_phone_short(self) -> None:
        assert validate_phone("123") is False

    def test_validate_price_valid(self) -> None:
        assert validate_price(10.99) is True

    def test_validate_price_negative(self) -> None:
        assert validate_price(-5) is False

    def test_validate_quantity_valid(self) -> None:
        assert validate_quantity(5) is True

    def test_validate_quantity_zero(self) -> None:
        assert validate_quantity(0) is False

    def test_validate_non_empty_string(self) -> None:
        assert validate_non_empty("hello") is True

    def test_validate_non_empty_none(self) -> None:
        assert validate_non_empty(None) is False

    def test_validate_non_empty_empty_string(self) -> None:
        assert validate_non_empty("") is False
