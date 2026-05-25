from __future__ import annotations

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class DimCategory(Base):
    __tablename__ = "dim_categories"
    __table_args__ = {"schema": "warehouse"}

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), nullable=False)
    description = Column(String(255))


class DimProduct(Base):
    __tablename__ = "dim_products"
    __table_args__ = {"schema": "warehouse"}

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("warehouse.dim_categories.category_id"))
    price = Column(Float)
    description = Column(String(500))
    is_active = Column(Integer, default=1)

    category = relationship("DimCategory")


class DimUser(Base):
    __tablename__ = "dim_users"
    __table_args__ = {"schema": "warehouse"}

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(200))
    email = Column(String(255))
    phone = Column(String(50))
    country = Column(String(100))
    city = Column(String(100))
    postal_code = Column(String(20))


class DimDate(Base):
    __tablename__ = "dim_dates"
    __table_args__ = {"schema": "warehouse"}

    date_id = Column(Date, primary_key=True)
    date = Column(Date, nullable=False)
    year = Column(Integer)
    month = Column(Integer)
    quarter = Column(Integer)
    day_of_week = Column(Integer)
    week_of_year = Column(Integer)


class FctSale(Base):
    __tablename__ = "fct_sales"
    __table_args__ = {"schema": "warehouse"}

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("warehouse.dim_products.product_id"))
    user_id = Column(Integer, ForeignKey("warehouse.dim_users.user_id"))
    date_id = Column(Date, ForeignKey("warehouse.dim_dates.date_id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_amount = Column(Float)
    discount = Column(Float, default=0.0)

    product = relationship("DimProduct")
    user = relationship("DimUser")
    date = relationship("DimDate")
