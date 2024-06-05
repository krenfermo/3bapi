## JOAQUIN MORA SANDRIA
# FastAPI Orders API 3b

Ejercicio:
Crear una aplicación en Python (usando el framework de tu elección si lo consideras necesario: Django, FastAPI, etc.) que cumpla con los siguientes requisitos:

# Requisitos:


- Python:
  - FastAPI
  - SQL Alchemy
- Docker 
- Pytest
- Database (Sqlite)
- Git



## To-dos:
# Exponer una API REST con los siguientes endpoints:
- /api/products (POST): para crear un nuevo producto con sku y name . Un nuevo producto siempre se crea con un stock de inicio de 100.
- /api/inventories/product/{PRODUCT_ID} (PATCH): para agregar stock al producto
- /api/orders (POST): para comprar productos
    - Agregar un job que dispara una alerta (puede ser un log en la consola) cuando el stock de un producto llega a ser inferior a 10.
- Agregar pruebas unitarias
- Compartir documentación de la API con Swagger o Postman Opcional:
- Empaquetar aplicación en un contenedor Docker



## Directorio app:
- crud.py
- database.py
- main.py
- models.py
- products.db
- schemas.py
- test_main.py



git clone https://github.com/krenfermo/3bapi.git


docker build -t myapi3b .

docker run -d --name contapi -p 8000:8000 myapi3b
