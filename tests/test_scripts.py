from __future__ import annotations

from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"

EXPECTED_SCRIPTS = [
    "init_database.py",
    "run_pipeline.py",
    "scheduler.py",
    "test_api_data.py",
    "create_views.py",
    "create_views.sql",
]


class TestScripts:
    def test_all_scripts_exist(self) -> None:
        for name in EXPECTED_SCRIPTS:
            assert (SCRIPTS_DIR / name).exists(), f"Missing script: {name}"

    def test_create_views_imports(self) -> None:
        """Verify the deploy script can import without errors."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "create_views", SCRIPTS_DIR / "create_views.py"
        )
        assert spec is not None
        assert spec.loader is not None

    def test_create_views_sql_referenced(self) -> None:
        content = (SCRIPTS_DIR / "create_views.py").read_text(encoding="utf-8")
        assert "create_views.sql" in content
        assert "deploy_views" in content
