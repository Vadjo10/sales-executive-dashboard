from __future__ import annotations

import re
from pathlib import Path

import pytest

SQL_PATH = Path(__file__).resolve().parent.parent / "scripts" / "create_views.sql"

EXPECTED_VIEWS = [
    "v_sales_summary",
    "v_monthly_sales",
    "v_customer_analysis",
    "v_product_performance",
    "v_daily_sales",
]

EXPECTED_COLUMNS = {
    "v_sales_summary": [
        "cart_id", "sale_date", "product_id", "product_name",
        "category", "unit_price", "quantity", "total_amount",
        "user_id", "user_name", "year_month",
    ],
    "v_monthly_sales": [
        "year", "month", "year_month", "total_transactions",
        "total_revenue", "avg_ticket", "active_customers",
    ],
    "v_customer_analysis": [
        "user_id", "user_name", "total_orders", "total_spent",
        "avg_order_value", "first_purchase_date", "last_purchase_date",
    ],
    "v_product_performance": [
        "product_id", "product_name", "category", "total_units_sold",
        "total_revenue", "unique_customers",
    ],
    "v_daily_sales": [
        "sale_date", "transactions", "revenue", "active_users",
    ],
}


@pytest.fixture
def sql_content() -> str:
    assert SQL_PATH.exists(), f"SQL file not found: {SQL_PATH}"
    return SQL_PATH.read_text(encoding="utf-8")


class TestViewsSQL:
    def test_file_exists(self) -> None:
        assert SQL_PATH.exists()

    def test_all_expected_views_present(self, sql_content: str) -> None:
        for view_name in EXPECTED_VIEWS:
            pattern = rf"CREATE OR REPLACE VIEW warehouse\.{view_name}\b"
            assert re.search(pattern, sql_content), f"Missing view: {view_name}"

    def test_each_view_has_comment(self, sql_content: str) -> None:
        for view_name in EXPECTED_VIEWS:
            pattern = rf"COMMENT ON VIEW warehouse\.{view_name}"
            assert re.search(pattern, sql_content), (
                f"Missing COMMENT for view: {view_name}"
            )

    def test_sql_has_valid_structure(self, sql_content: str) -> None:
        create_count = len(re.findall(
            r"CREATE OR REPLACE VIEW", sql_content, re.IGNORECASE
        ))
        assert create_count == len(EXPECTED_VIEWS), (
            f"Expected {len(EXPECTED_VIEWS)} CREATE VIEW statements, found {create_count}"
        )

    def test_expected_columns_in_views(self, sql_content: str) -> None:
        for view_name, expected_cols in EXPECTED_COLUMNS.items():
            match = re.search(
                rf"CREATE OR REPLACE VIEW warehouse\.{view_name}\s+AS\s+(.+?)(?:;|\nCREATE|\Z)",
                sql_content,
                re.DOTALL,
            )
            assert match, f"Could not extract body for {view_name}"
            body = match.group(1)
            for col in expected_cols:
                assert col in body, (
                    f"Column '{col}' not found in view {view_name}"
                )

    def test_no_hardcoded_credentials(self, sql_content: str) -> None:
        sensitive = ["password", "senha", "secret"]
        for word in sensitive:
            assert word not in sql_content.lower(), (
                f"Sensitive word found in SQL: {word}"
            )

    def test_schemas_are_correct(self, sql_content: str) -> None:
        assert "warehouse." in sql_content
        assert "staging." in sql_content
