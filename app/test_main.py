
from main import app
from database import get_db, Base
 

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"API": "Running!!"}
    
  
def  test_create_products():
    response= client.post("/api/products/",
        json={
            "product_sku": "sku_1000",
            "product_name": "Mesa Redonda",
            "product_price": 12500,
            "product_stock": 100
            },)
    
    assert response.status_code == 200
    assert response.json() == 	{
                                "product_sku": "sku_1000",
                                "product_name": "Mesa Redonda",
                                            "product_price": 12500,
                                            "product_stock": 100
                                }
 
def  test_create_products_same():

    response= client.post("/api/products/",
        json={
            "product_sku": "sku_1000",
            "product_name": "Mesa Redonda",
            "product_price": 12500,
            "product_stock": 100
            },)
    
    assert response.status_code == 400
    assert response.json() == 	{
                                "detail": "Producto existe"
                                }
    
    
    
def test_Show_Products_Get():
    response = client.get("/api/show_products")

    assert response.status_code == 200
    assert response.json() == [
                {   "is_active": True,
                    "product_id": 1,
                    "product_sku": "sku_1000",
                    "product_name": "Mesa Redonda",
                    "product_price": 12500,
                    "product_stock": 100
                                }
                ]
    


def  test_agregar_stock_not_found():
    PRODUCT_ID=5
    response= client.patch("/api/inventories/product/5",
        json={"PRODUCT_ID":PRODUCT_ID,
            "stock_a_ingresar": 100
            },)
    
    assert response.status_code == 404
    assert response.json() == 	{
                                "detail": 'Producto no encontrado con el ID: 5'
                                }
 

def  test_agregar_stock():
    response= client.patch("/api/inventories/product/1",
        json=    {
  "stock_a_ingresar": 1
},)
    
    assert response.status_code == 200
    assert response.json() == 	{
            "product_id": 1,
            "product_sku": "sku_1000",
            "product_name": "Mesa Redonda",
            "product_price": 12500,
            "product_stock": 101,
            "is_active": True
}
    
 
def  test_comprar_producto():
    
    
    response= client.post("/api/orders/",
        json={
            "product_id": 1,
            "cantidad": 11
            },)
    
    assert response.status_code == 200
    assert response.json() == 	{
                            "product_sku": "sku_1000",
                                "product_name": "Mesa Redonda",
                                            "product_price": 12500,
                                            "product_stock": 90
                                }


def  test_comprar_producto_NOSTOCK():
    response= client.post("/api/orders/",
        json={
            "product_id": 1,
            "cantidad": 205
            },)
    
    assert response.status_code == 400
    assert response.json() == 	{
                            "detail": "NO HAY STOCK PARA ESA OPERACION"
                                }
    
def  test_comprar_producto_NO_Found():
    response= client.post("/api/orders/",
        json={
            "product_id": 2,
            "cantidad": 1
            },)
    
    assert response.status_code == 400
    assert response.json() == 	{
                            "detail": "Producto NO existe"
                                }    
 
 
