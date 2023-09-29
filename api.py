import logging
from fastapi import FastAPI
import uvicorn as uv
from database import Database
from schemas import User, Product, Order
import config

logging.basicConfig(level=logging.DEBUG, filename=config.LOG_FILE,
                    filemode="a", format='%(asctime)s - %(name)s - '
                    '%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

api = FastAPI()

db = Database()

# Начальная страница при запуске приложения
@api.get("/")
def root():
    return {"Enter /{users, products, orders}, to get the list users, products or orders"
            }

# Получить список пользователей
@api.get("/users")
def get_users(limit: int = 1, offset: int = 0, city: str = None):
    return db.get_users(limit, offset, city)

# Получить список продуктов
@api.get("/products")
def get_products(limit: int = 1, offset: int = 0, seller: str = None):
    return db.get_products(limit, offset, seller)

# Получить список заказов
@api.get("/orders")
def get_orders(limit: int = 1, offset: int = 0, user_id: int = None):
    return db.get_orders(limit, offset, user_id)

# Добавит пользователя
@api.post("/user/")
def add_user(user: User):
    return db.add_user(user.username, user.phone, user.address, user.email)

# Добавить продукт
@api.post("/product/")
def add_product(product: Product):
    return db.add_product(product.name, product.seller, product.price)

# Добавить заказ
@api.post("/order/")
def add_order(order: Order):
    return db.add_order(order.user_id, order.product_id, order.count)

# Изменить пользователя
@api.put("/upd_users/{user_id}")
def update_user(user_id: int, user: User):
    return db.update_user(user_id, user.username, user.phone, user.address, user.email)

# Изменить продукт
@api.put("/upd_products/{product_id}")
def update_product(product_id: int, product: Product):
    return db.update_product(product_id, product.name, product.seller, product.price)

# Изменить заказ
@api.put("/upd_orders/{order_id}")
def update_order(order_id: int, order: Order):
    return db.update_order(order_id, order.user_id, order.product_id, order.count)

# Удалить пользовтеля
@api.delete("/d_user/{user_id}")
def delete_user(user_id: int):
    return db.delete_user(user_id)

# Удалить продукт
@api.delete("/d_product/{product_id}")
def delete_product(product_id: int):
    return db.delete_product(product_id)

# Удалить заказ
@api.delete("/d_order/{order_id}")
def delete_order(order_id : int):
    return db.delete_order(order_id)

if __name__ == '__main__':
    db.create_database()

    uv.run(
        "api:api",
        host='localhost',
        port=8000,
        reload=True
    )
