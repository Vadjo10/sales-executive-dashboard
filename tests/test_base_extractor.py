from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.extractors.base_extractor import BaseExtractor
from src.extractors.fake_store_extractor import FakeStoreExtractor


class TestBaseExtractor:
    def test_validate_response_none(self) -> None:
        extractor = FakeStoreExtractor(api_client=MagicMock())
        result = extractor.validate_response(None)
        assert result == []

    def test_validate_response_not_list(self) -> None:
        extractor = FakeStoreExtractor(api_client=MagicMock())
        result = extractor.validate_response({"id": 1})
        assert result == []

    def test_validate_response_valid_list(self) -> None:
        extractor = FakeStoreExtractor(api_client=MagicMock())
        result = extractor.validate_response([{"id": 1}])
        assert result == [{"id": 1}]
