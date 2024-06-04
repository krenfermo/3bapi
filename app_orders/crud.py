from uuid import uuid4

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from schemas import *
from models import *

 
async def create_product(db: Session, producto:ProductSchema):
    try:
        new_product=None
        with db.begin():

    
            new_product = Products(product_sku=producto.product_sku,
                                   product_name=producto.product_name,
                                   product_price=producto.product_price,
                                   product_stock=producto.product_stock)
            db.add(new_product)
            db.commit()
            db.flush(new_product)
             
    except Exception as error:
        print("ERROR:",error)
    return new_product


async def get_product_by_sku(db: Session, sku: str):
    with db.begin():

        product=db.query(Products).filter(Products.product_sku == sku).first()

    return product

