from pydantic import UUID4, BaseModel

class ProductSchema(BaseModel): 
   
    product_sku : str
    product_name : str
    product_price : float
    product_stock: int=100
         
    
    class Config:
        orm_mode = True
        

class ProductInventarySchema(BaseModel): 

    stock_a_ingresar: int
         
    
    class Config:
        orm_mode = True