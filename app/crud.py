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


async def crea_order(db: Session, producto:OrderSchema):
    new_order=None
     
    print(producto)
    #update_data = producto.dict(exclude_unset=True)
    new_order = Orders(product_id=producto["product_id"],
                        cantidad=producto["cantidad"])
    db.add(new_order)
    #db.commit()
    
    print("pasa1")
    return new_order
                    
                    
async def compra_product(db: Session, producto:OrderSchema):
    try:
        new_order=None
        with db.begin():

            update_data = producto.dict(exclude_unset=True)
            
            db_product=db.query(Products).filter(Products.product_id == producto.product_id).first()
            
           
            new_stock=db_product.product_stock - update_data["cantidad"]
            print(new_stock)
            if new_stock>=0 :
                
                if new_stock<10:
                    print('el producto {} solo tiene {} en stock'.format(db_product.product_name,new_stock))
                
                db.query(Products).filter(Products.product_id == producto.product_id).update({"product_stock": (new_stock)})
                
                new_order=await crea_order(db,update_data)
      
                db.commit()
                db.flush(db_product)
                db.flush(new_order)
                print("pasa")
            else:
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
