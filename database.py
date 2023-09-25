from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, ForeignKey, select
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from tables import Order, User, Product
from fastapi.responses import JSONResponse

class Database:
    def __init__(self):
        self.DatabaseUri = f"postgresql://postgres:1@localhost:5432/store"
        self.engine = create_engine(self.DatabaseUri)


    def create_database(self):
        if database_exists(self.DatabaseUri) is False:
            create_database(self.DatabaseUri)

        metadata = MetaData()
        users_table = Table('users', metadata,
                            Column("id", Integer, primary_key=True),
                                  Column("username", String),
                                  Column("phone", String),
                                  Column("address", String),
                                  Column("email",String)
                             )

        product_table = Table('products', metadata,
                              Column("id", Integer, primary_key=True),
                              Column("name", String),
                              Column("seller", String),
                              Column("price", Float),
                              )

        order_table = Table('orders', metadata,
                            Column("id", Integer, primary_key=True),
                            Column('user_id', Integer, ForeignKey("users.id")),
                            Column('product_id', Integer, ForeignKey("products.id")),
                            Column('count', Integer)
                            )

        metadata.drop_all(self.engine)
        metadata.create_all(self.engine)

    def append(self, user_list, product_list, order_list):
        self.create_database()
        Session = sessionmaker(self.engine)
        session = Session()

        user = User(username="Name", phone="11111111", address="idfjhjfsfjhyulksoikf", email="1@gmail.com")
        session.add(user)

        user_list.append(user)

        prod1 = Product(name="Cheese", seller="Ivanov", price=600)
        prod2 = Product(name="Milk", seller="Petrov", price=100)
        session.add_all([prod1, prod2])
        product_list.append(prod1)
        product_list.append(prod2)

        order1 = Order(user=user, product=prod1, count=5)
        order2 = Order(user=user, product=prod2, count=10)
        order_list.append(order1)
        order_list.append(order2)
        session.add_all([order1, order2])

        session.commit()
        session.close()

    def get_users(self, limit, offset, city):
        Session = sessionmaker(self.engine)
        session = Session()
        results = ''
        if city:
            results = session.query(User).filter(User.address.ilike(f"%{city}%")).limit(limit).offset(offset).all()
        else:
            results = session.query(User).limit(limit).offset(offset).all()
        session.close()
        return results

    def get_products(self, limit, offset, seller):
        Session = sessionmaker(self.engine)
        session = Session()
        results = ''
        if seller:
            results = session.query(Product).filter(Product.seller == seller).limit(limit).offset(offset).all()
        else:
            results = session.query(Product).limit(limit).offset(offset).all()

        session.close()
        return results

    def get_orders(self, limit, offset, user_id):
        Session = sessionmaker(self.engine)
        session = Session()

        results = ''
        if user_id:
            results = session.query(Order).filter(Order.user_id == user_id).limit(limit).offset(offset).all()
        else:
            results = session.query(Order).limit(limit).offset(offset).all()

        session.close()
        return results

    def add_user(self, username, phone, address, email):
        Session = sessionmaker(self.engine)
        session = Session()

        user = User(username=username, phone=phone, address=address, email=email)
        session.add(user)
        session.commit()
        session.close()
        return user

    def add_product(self, name, seller, price):
        Session = sessionmaker(self.engine)
        session = Session()

        product = Product(name=name, seller=seller, price=price)
        session.add(product)
        session.commit()
        session.close()
        return product

    def add_order(self, user, product, count):
        Session = sessionmaker(self.engine)
        session = Session()

        order = Order(user=user, product=product, count=count)
        session.add(order)
        session.commit()
        session.close()
        return order

    def update_user(self, user_id, data):
        Session = sessionmaker(self.engine)
        session = Session()

        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return "Пользователь не найден"

        user.username = data['username']
        user.phone = data['phone']
        user.address = data['address']
        user.email = data['email']
        session.commit()
        session.refresh(user)
        return user

    def update_product(self, product_id, data):
        Session = sessionmaker(self.engine)
        session = Session()

        product = session.query(Product).filter(Product.id == product_id).first()
        if product == None:
            return "Продукт не найден"

        product.name = data['name']
        product.seller = data['seller']
        product.price = data['price']
        session.commit()
        session.refresh(product)
        return product

    def update_order(self, order_id, data):
        Session = sessionmaker(self.engine)
        session = Session()

        order = session.query(Order).filter(Order.id == order_id).first()
        if order == None:
            return "Заказ не найден"

        order.user = data['user']
        order.product = data['product']
        order.count = data['count']
        session.commit()
        session.refresh(order)
        return order

    def delete_user(self, user_id):
        Session = sessionmaker(self.engine)
        session = Session()

        user = session.query(User).filter(User.id == user_id).first()

        if user == None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})

        session.delete(user)
        session.commit()
        session.close()

    def delete_product(self, product_id):
        Session = sessionmaker(self.engine)
        session = Session()

        product = session.query(Product).filter(Product.id == product_id).first()

        if product == None:
            return JSONResponse(status_code=404, content={"message": "Продукт не найден"})

        session.delete(product)
        session.commit()
        session.close()

    def delete_order(self, order_id):
        Session = sessionmaker(self.engine)
        session = Session()

        order = session.query(Order).filter(Order.id == order_id).first()

        if order == None:
            return JSONResponse(status_code=404, content={"message": "Заказ не найден"})

        session.delete(order)
        session.commit()
        session.close()
