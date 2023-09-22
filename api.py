from fastapi import FastAPI
from database import Database
import uvicorn as uv

api = FastAPI()

db = Database()
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
@api.post("/user")
async def add_user(username: str = '_', phone: str = '0000000',
                   address: str = "Россия, город Москва, улица Ленина, дом 12, квартира 1", email: str = "_@gmail.com"):
    return db.add_user(username, phone, address, email)

if __name__ == '__main__':
    db.append([],[],[])

    uv.run(
        "api:api",
        host='localhost',
        port=8000,
        reload=True
    )
