from pydantic import UUID4, BaseModel

class ProductSchema(BaseModel): 
   
    product_sku : str
    product_name : str
    product_price : float
    product_stock: int=100
         
    
    class Config:
        from_attributes = True
        

class ProductInventarySchema(BaseModel): 

    stock_a_ingresar: int
    class Config:
        from_attributes = True
        
        
class OrderSchema(BaseModel): 
    product_id : int
    cantidad: int
    
    class Config:
        from_attributes = True