from fastapi import Depends, FastAPI, HTTPException,status
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from database import SessionLocal, engine,get_db

from models import *
from crud import *
from schemas import *
 

Base.metadata.create_all(bind=engine)

app = FastAPI()
  
        
@app.get("/")
async def root():
    return {"API": "Running!!"}


@app.post("/api/products/", response_model=ProductSchema)
async def a_create_product(producto: ProductSchema, db: Session = Depends(get_db)):
    respuesta =  await get_product_by_sku(db, sku=producto.product_sku)
    if respuesta:
        raise HTTPException(status_code=400, detail="Producto existe")
    response=await create_product(db=db, producto=producto)
    return response


@app.get('/api/show_products')
def Show_Products_Get(db: Session = Depends(get_db)):    
    from_limit=0
    to_limit=100
    result = db.query(Products).offset(from_limit).limit(to_limit).all()   
    return result


@app.patch('/api/inventories/product/{PRODUCT_ID}')
def agregar_stock(PRODUCT_ID: str, producto: ProductInventarySchema, db: Session = Depends(get_db)):
    product_query = db.query(Products).filter(Products.product_id == PRODUCT_ID)
    db_product = product_query.first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Producto no encontrado con el ID: {PRODUCT_ID}')
    update_data = producto.dict(exclude_unset=True)
    db.query(Products).filter(Products.product_id == PRODUCT_ID).update({"product_stock": (Products.product_stock +update_data["stock_a_ingresar"])})
    db.commit()
    db.refresh(db_product)
    return db_product


@app.post("/api/orders/", response_model=ProductSchema)
async def comprar_producto(producto: OrderSchema, db: Session = Depends(get_db)):
    respuesta =  await get_product_by_id(db, id=producto.product_id)
    if respuesta:
        response=await compra_product(db=db, producto=producto)
        if response!=False:  
            return response
        raise HTTPException(status_code=400, detail="NO HAY STOCK PARA ESA OPERACION")
    raise HTTPException(status_code=400, detail="Producto NO existe")


@app.get('/api/show_orders')
def Show_Orders_Get(db: Session = Depends(get_db)):    
    from_limit=0
    to_limit=100
    result = db.query(Orders).offset(from_limit).limit(to_limit).all()   
    return result