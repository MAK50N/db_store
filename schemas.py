from pydantic import BaseModel
class User(BaseModel):
    username: str
    phone: str
    address: str
    email: str

class Product(BaseModel):
    name: str
    seller: str
    price: float

class Order(BaseModel):
    user_id: int
    product_id: int
    count: int