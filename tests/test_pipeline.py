from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.pipeline import CHECKPOINT_DIR, Pipeline
from src.utils.exceptions import PipelineError


@pytest.fixture
def pipeline() -> Pipeline:
    mock_extractor = MagicMock()
    mock_cleaner = MagicMock()
    mock_enricher = MagicMock()
    mock_loader = MagicMock()
    pipe = Pipeline(
        extractor=mock_extractor,
        cleaner=mock_cleaner,
        enricher=mock_enricher,
        loader=mock_loader,
        checkpoint=False,
    )
    return pipe


def test_pipeline_run_success(pipeline: Pipeline) -> None:
    pipeline.extractor.extract_all.return_value = {
        "products": [{"id": 1, "title": "A", "price": 10, "description": "d", "category": "c"}],
        "categories": ["electronics"],
        "users": [{"id": 1, "email": "a@b.com", "username": "u"}],
        "carts": [{"id": 1, "userId": 1, "date": "2024-01-01", "products": []}],
    }
    dummy_df = pd.DataFrame({"id": [1]})
    pipeline.cleaner.transform.return_value = dummy_df
    pipeline.enricher.transform.return_value = dummy_df
    pipeline.loader.load_all.return_value = {"products": 1, "users": 1, "carts": 1}

    result = pipeline.run()
    assert result["status"] == "success"
    assert "run_id" in result


def test_pipeline_run_failure(pipeline: Pipeline) -> None:
    pipeline.extractor.extract_all.side_effect = Exception("Extraction failed")
    with pytest.raises(PipelineError):
        pipeline.run()


def test_pipeline_checkpoint_created(pipeline: Pipeline) -> None:
    pipeline.checkpoint = True
    pipeline.extractor.extract_all.return_value = {
        "products": [{"id": 1, "title": "A", "price": 10, "description": "d", "category": "c"}],
        "categories": ["electronics"],
        "users": [{"id": 1, "email": "a@b.com", "username": "u"}],
        "carts": [{"id": 1, "userId": 1, "date": "2024-01-01", "products": []}],
    }
    dummy_df = pd.DataFrame({"id": [1]})
    pipeline.cleaner.transform.return_value = dummy_df
    pipeline.enricher.transform.return_value = dummy_df
    pipeline.loader.load_all.return_value = {"products": 1}

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("src.pipeline.CHECKPOINT_DIR", Path(tmpdir) / "checkpoints"):
            result = pipeline.run()
            assert result["status"] == "success"
            checkpoint_path = Path(tmpdir) / "checkpoints" / result["run_id"]
            checkpoint_files = list(checkpoint_path.glob("*.parquet"))
            assert len(checkpoint_files) > 0
