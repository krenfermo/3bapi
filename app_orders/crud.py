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


 
async def compra_product(db: Session, producto:OrderSchema):
    try:
         
        with db.begin():

            update_data = producto.dict(exclude_unset=True)
            
            db_product=db.query(Products).filter(Products.product_id == producto.product_id).first()
            
           
            new_stock=db_product.product_stock - update_data["cantidad"]
          
            if new_stock>0 :
                
                if new_stock<10:
                    print('el producto {} solo tiene {} en stock'.format(db_product.product_name,new_stock))
                db.query(Products).filter(Products.product_id == producto.product_id).update({"product_stock": (new_stock)})
                
                db.commit()
                
        
                db.flush(db_product)
                with db.begin():
                    
                        new_order=None
                    
                        new_order = Orders(product_id=update_data["product_id"],
                                            cantidad=update_data["cantidad"])
                        db.add(new_order)
                        db.commit()
                        db.flush(new_order)
            
            return False
    except Exception as error:
        print("ERROR:",error)
    return db_product




async def get_product_by_sku(db: Session, sku: str):
    with db.begin():
        product=db.query(Products).filter(Products.product_sku == sku).first()

    return product


async def get_product_by_id(db: Session, id: int):
    with db.begin():
        product=db.query(Products).filter(Products.product_id == id).first()

    return product
