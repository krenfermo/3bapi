from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class Products(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_sku = Column(String)
    product_name = Column(String, unique=True)
    product_price = Column(Float)
    product_stock = Column(Integer)
    is_active = Column(Boolean, default=True)


class Orders(Base):
    __tablename__ = "products_orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    order_date = Column(DateTime)
    product_id = Column(String)
