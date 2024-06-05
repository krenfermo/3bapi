from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,DateTime
from sqlalchemy.orm import relationship

from database import Base
import datetime

class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_sku = Column(String)
    product_name = Column(String, unique=True)
    product_price = Column(Float)
    product_stock = Column(Integer)
    is_active = Column(Boolean, default=True)
    
class Orders(Base):
    __tablename__ = "products_orders"

    order_id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    product_id = Column(Integer)
    cantidad= Column(Integer)

 