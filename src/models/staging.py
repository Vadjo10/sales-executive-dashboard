from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class StgApiProduct(Base):
    __tablename__ = "stg_api_products"
    __table_args__ = {"schema": "staging"}

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    price = Column(Float)
    description = Column(Text)
    category = Column(String(100))
    image = Column(String(500))
    rating_rate = Column(Float)
    rating_count = Column(Integer)


class StgApiUser(Base):
    __tablename__ = "stg_api_users"
    __table_args__ = {"schema": "staging"}

    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    username = Column(String(100))
    password = Column(String(255))
    phone = Column(String(50))
    name_firstname = Column(String(100))
    name_lastname = Column(String(100))
    address_city = Column(String(100))
    address_street = Column(String(255))
    address_number = Column(Integer)
    address_zipcode = Column(String(20))
    address_geolocation_lat = Column(String(20))
    address_geolocation_long = Column(String(20))


class StgApiCart(Base):
    __tablename__ = "stg_api_carts"
    __table_args__ = {"schema": "staging"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    date = Column(DateTime)
    products = Column(Text)


class StgApiCategory(Base):
    __tablename__ = "stg_api_categories"
    __table_args__ = {"schema": "staging"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
