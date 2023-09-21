from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

class Order(Base):
    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    product_id = Column(Integer, ForeignKey("Products.id"))
    count = Column(Integer)
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    phone = Column(String)
    address = Column(String)
    email = Column(String)
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    seller = Column(String)
    price = Column(Integer)
    orders = relationship("Order", back_populates="product")

