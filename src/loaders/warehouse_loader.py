from __future__ import annotations

import json
from typing import Any

import pandas as pd

from src.loaders.database import Database
from src.logger import logger
from src.utils.exceptions import DatabaseOperationError
from src.utils.helpers import timer


class WarehouseLoader:
    def __init__(self, database: Database | None = None) -> None:
        self.db = database or Database()

    def _truncate_all(self) -> None:
        logger.info("Truncating warehouse tables...")
        self.db.execute("TRUNCATE TABLE warehouse.fct_sales CASCADE")
        self.db.execute("TRUNCATE TABLE warehouse.dim_products CASCADE")
        self.db.execute("TRUNCATE TABLE warehouse.dim_categories CASCADE")
        self.db.execute("TRUNCATE TABLE warehouse.dim_users CASCADE")
        logger.info("Warehouse tables truncated")

    def load_dim_categories(self) -> int:
        logger.info("Loading dim_categories...")
        df = pd.read_sql(
            "SELECT name FROM staging.stg_api_categories ORDER BY name",
            self.db.engine,
        )
        if df.empty:
            logger.warning("No categories to load")
            return 0

        df = df.rename(columns={"name": "category_name"}).reset_index(names=["category_id"])
        df["category_id"] = df["category_id"] + 1
        df["description"] = None
        df.to_sql(
            "dim_categories",
            self.db.engine,
            schema="warehouse",
            if_exists="append",
            index=False,
            method="multi",
        )
        logger.info(f"Loaded {len(df)} categories into dim_categories")
        return len(df)

    def load_dim_products(self) -> int:
        logger.info("Loading dim_products...")
        products = pd.read_sql(
            """SELECT id, title, price, description, category
            FROM staging.stg_api_products ORDER BY id""",
            self.db.engine,
        )
        if products.empty:
            logger.warning("No products to load")
            return 0

        categories = pd.read_sql(
            "SELECT category_id, category_name FROM warehouse.dim_categories",
            self.db.engine,
        )
        merged = products.merge(
            categories,
            left_on="category",
            right_on="category_name",
            how="left",
        )
        dim_products = merged.rename(
            columns={
                "id": "product_id",
                "title": "product_name",
            }
        )
        dim_products["is_active"] = 1
        dim_products = dim_products[
            ["product_id", "product_name", "category_id", "price", "description", "is_active"]
        ]

        dim_products.to_sql(
            "dim_products",
            self.db.engine,
            schema="warehouse",
            if_exists="append",
            index=False,
            method="multi",
        )
        logger.info(f"Loaded {len(dim_products)} products into dim_products")
        return len(dim_products)

    def load_dim_users(self) -> int:
        logger.info("Loading dim_users...")
        import json
        df = pd.read_sql(
            "SELECT id, email, username, name, address, phone FROM staging.stg_api_users ORDER BY id",
            self.db.engine,
        )
        if df.empty:
            logger.warning("No users to load")
            return 0

        rows: list[dict[str, Any]] = []
        for _, row in df.iterrows():
            name_data = {}
            addr_data = {}
            try:
                if row["name"] and not pd.isna(row["name"]):
                    name_data = json.loads(row["name"])
            except (json.JSONDecodeError, TypeError):
                pass
            try:
                if row["address"] and not pd.isna(row["address"]):
                    addr_data = json.loads(row["address"])
            except (json.JSONDecodeError, TypeError):
                pass

            first = name_data.get("firstname", "")
            last = name_data.get("lastname", "")
            user_name = f"{first} {last}".strip() or row["username"]

            rows.append(
                {
                    "user_id": row["id"],
                    "user_name": user_name,
                    "email": row["email"],
                    "phone": row["phone"],
                    "country": "Unknown",
                    "city": addr_data.get("city", "Unknown"),
                    "postal_code": addr_data.get("zipcode", "00000"),
                }
            )

        dim_users = pd.DataFrame(rows)
        dim_users.to_sql(
            "dim_users",
            self.db.engine,
            schema="warehouse",
            if_exists="append",
            index=False,
            method="multi",
        )
        logger.info(f"Loaded {len(dim_users)} users into dim_users")
        return len(dim_users)

    @timer
    def load_fct_sales(self) -> int:
        logger.info("Loading fct_sales...")
        carts = pd.read_sql(
            "SELECT id, userid AS user_id, date, products FROM staging.stg_api_carts ORDER BY id",
            self.db.engine,
        )
        if carts.empty:
            logger.warning("No carts to load")
            return 0

        products = pd.read_sql(
            "SELECT product_id, price FROM warehouse.dim_products",
            self.db.engine,
        )

        rows: list[dict[str, Any]] = []
        for _, cart in carts.iterrows():
            cart_id = cart["id"]
            user_id = cart["user_id"]
            sale_date = pd.Timestamp(cart["date"]).date()

            raw_products = cart["products"]
            if not raw_products or pd.isna(raw_products):
                continue

            try:
                items = (
                    json.loads(raw_products)
                    if isinstance(raw_products, str)
                    else raw_products
                )
            except (json.JSONDecodeError, TypeError):
                logger.warning(f"Could not parse products for cart {cart_id}")
                continue

            for item in items:
                product_id = item.get("productId") if isinstance(item, dict) else item.get("productId")
                quantity = int(item.get("quantity", 1)) if isinstance(item, dict) else 1

                price_row = products[products["product_id"] == product_id]
                unit_price = float(price_row["price"].iloc[0]) if not price_row.empty else 0.0

                rows.append(
                    {
                        "product_id": product_id,
                        "user_id": user_id,
                        "date_id": sale_date,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total_amount": round(unit_price * quantity, 2),
                        "discount": 0.0,
                    }
                )

        if not rows:
            logger.warning("No sale records generated")
            return 0

        fct_sales = pd.DataFrame(rows)
        fct_sales.to_sql(
            "fct_sales",
            self.db.engine,
            schema="warehouse",
            if_exists="append",
            index=False,
            method="multi",
        )
        logger.info(f"Loaded {len(fct_sales)} sales records into fct_sales")
        return len(fct_sales)

    @timer
    def run_all(self) -> dict[str, int]:
        logger.info("Starting warehouse load...")
        self._truncate_all()
        results: dict[str, int] = {}
        results["dim_categories"] = self.load_dim_categories()
        results["dim_products"] = self.load_dim_products()
        results["dim_users"] = self.load_dim_users()
        results["fct_sales"] = self.load_fct_sales()
        logger.info(f"Warehouse load completed: {results}")
        return results
