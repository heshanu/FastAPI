from typing import Union
from fastapi import FastAPI,status,Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from model.ProductModel import Product
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import DATABASE_CONFIG

app = FastAPI()

def get_db_connection():
    try:
        connection = psycopg2.connect(**DATABASE_CONFIG)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/")
def readItems():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM products")
        items = cursor.fetchall()
        if not items:
            raise HTTPException(status_code=404, detail='Couldnt find products')
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/product/{id}")
def getProduct(id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        item = cursor.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/products/{id}")
def deleteProductById(id:int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("select FROM products WHERE id = %s", (id,))
        product=cursor.fetchone()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        cursor.execute("Delete from products where id=%s",(id,))
        conn.commit()
        return {"message":f"Successfuly delete product id:{id}"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.put("/product/{id}", status_code=status.HTTP_200_OK)
def updateProductById(id: int, product: Product):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        item = cursor.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Product not found")
        cursor.execute(
            "UPDATE products SET name = %s, price = %s, is_sale = %s, inventory = %s WHERE id = %s",
            (product.name, product.price, product.is_sale, product.inventory, id)
        )
        conn.commit()
        return {"message": f"Successfully updated product id: {id}"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
