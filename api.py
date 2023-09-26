from fastapi import FastAPI
from database import Database
import uvicorn as uv
from pydantic import BaseModel

api = FastAPI()

db = Database()

class User(BaseModel):
    username: str
    phone: str
    address: str
    email: str

class Product(BaseModel):
    name: str
    seller: str
    price: float

@api.get("/")
async def root():
    return {"Enter /{users, products, orders}, to get the list users, products or orders"
            }

@api.get("/users")
async def get_users(limit: int = 1, offset: int = 0, city: str = None):
    return db.get_users(limit, offset, city)

@api.get("/products")
async def get_products(limit: int = 1, offset: int = 0, seller: str = None):
    return db.get_products(limit, offset, seller)

@api.get("/orders")
async def get_orders(limit: int = 1, offset: int = 0, user_id: int = None):
    return db.get_orders(limit, offset, user_id)
@api.post("/user/")
async def add_user(user: User):
    return db.add_user(user.username, user.phone, user.address, user.email)

@api.post("/product/")
async def add_product(product: Product):
    return db.add_product(product.name, product.seller, product.price)

@api.post("/order/")
async def add_order(user_id: int, product_id: int, count: int):
    return db.add_order(user_id, product_id, count)

@api.put("/upd_users/{user_id}")
def update_user(user_id: int, user: User):
    return db.update_user(user_id, user.username, user.phone, user.address, user.email)

@api.put("/upd_products/{product_id}")
def update_product(product_id: int, product: Product):
    return db.update_product(product_id, product.name, product.seller, product.price)

@api.put("/upd_orders/{order_id}")
def update_order(order_id: int, user_id: int, product_id: int, count: int):
    return db.update_order(order_id, user_id, product_id, count)

@api.delete("/d_user/{user_id}")
async def delete_user(user_id: int):
    return db.delete_user(user_id)

@api.delete("/d_product/{product_id}")
async def delete_user(product_id: int):
    return db.delete_user(product_id)

@api.delete("/d_order/{order_id}")
async def delete_user(order_id : int):
    return db.delete_user(order_id)

if __name__ == '__main__':
    db.append([],[],[])

    uv.run(
        "api:api",
        host='localhost',
        port=8000,
        reload=True
    )
