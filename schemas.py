from pydantic import BaseModel

# схема пользователя
class User(BaseModel):
    username: str
    phone: str
    address: str
    email: str

# схема продукта
class Product(BaseModel):
    name: str
    seller: str
    price: float

# схема заказа
class Order(BaseModel):
    user_id: int
    product_id: int
    count: int
