from fastapi import FastAPI
from database import Database
from tables import Order, User, Product
from sqlalchemy.orm import sessionmaker
from tables import User, Product

if __name__ == '__main__':
    db = Database()
    db.create_database()
    Session = sessionmaker(db.engine)
    session = Session()

    user_list = []
    user = User(username="Name", phone="11111111", address="idfjhjfsfjhyulksoikf", email="1@gmail.com")
    session.add(user)
    # user = session.query(User).filter(User.username == "Name").first()

    # user_list.append(user)

    product_list = []
    prod1 = Product(name="Cheese", seller="Ivanov", price=600)
    prod2 = Product(name="Milk", seller="Petrov", price=100)
    session.add_all([prod1, prod2])
    # product_list.append(prod1)
    # product_list.append(prod2)

    order_list = []
    order1 = Order(user=user, product=prod1, count=5)
    order2 = Order(user=user, product=prod2, count=10)
    # order_list.append(order1)
    # order_list.append(order2)

    session.add_all([order1, order2])
    session.commit()
    session.close()

    # db.append(user_list, product_list, order_list)
