from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

Base = declarative_base()

# Модель таблицы заказов
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    count = Column(Integer)
    user = relationship("User", backref="orders")
    product = relationship("Product", backref="orders")

# Модель таблицы пользователей
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    phone = Column(String)
    address = Column(String)
    email = Column(String)

# Модель таблицы продуктов
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    seller = Column(String)
    price = Column(Float)
