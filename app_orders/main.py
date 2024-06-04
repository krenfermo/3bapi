from fastapi import Depends, FastAPI, HTTPException
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
    print(respuesta)
    if respuesta:
        raise HTTPException(status_code=400, detail="Producto existe")
    print("pasa")
    response=await create_product(db=db, producto=producto)
    print(response)
    return response



@app.get('/api/show_products')
def Show_Products_Get(db: Session = Depends(get_db)):    
    from_limit=0
    to_limit=100
    result = db.query(Products).offset(from_limit).limit(to_limit).all()   
    return result

