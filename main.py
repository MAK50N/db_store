from fastapi import FastAPI
from database import Database
from tables import Order, User, Product
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    db = Database()
    db.create_database()
    Session = sessionmaker(db.engine)
    session = Session()

    user_list = []
    user = User(username="Makson", phone="11111111", address="idfjhjfsfjhyulksoikf", email="1@gmail.com")
    user_list.append(user)

    product_list = []
    prod1 = Product(name="Cheese", seller="Ivanov", price=600)
    prod2 = Product(name="Milk", seller="Petrov", price=100)
    product_list.append(prod1)
    product_list.append(prod2)

    order_list = []
    order1 = Order(count=5)
    order1.user = user
    order1.product = prod1

    order2 = Order(count=10)
    order2.user = user
    order2.product = prod2

    order_list.append(order1)
    order_list.append(order2)

    session.add_all([user, prod1, order1])
    session.add_all([prod2, order2])
    session.commit()
    session.close()

    # db.append(user_list, product_list, order_list)
