from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from fastapi.responses import JSONResponse
from tables import Order, User, Product


import config


class Database:
    def __init__(self):
        self.DatabaseUri = config.database_uri
        self.engine = create_engine(self.DatabaseUri)

    # Создае базу данных и таблицы юзеров, продукты и заказов
    def create_database(self):
        if database_exists(self.DatabaseUri) is False:
            create_database(self.DatabaseUri)

        metadata = MetaData()

        metadata.drop_all(self.engine)
        metadata.create_all(self.engine)

    # Получает список юзеров определенного лимита, начиная с какой либо строки, и если передан city,
    # переданной через пременную offset, то из определенного города
    def get_users(self, limit, offset, city):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            results = session.query(User).limit(limit).offset(offset).all()
        except:
            JSONResponse(status_code=404, content={'message': "Ошибка"})

        for element in results[:]:
            if element.address.find("Москва") == -1:
                results.remove(element)

        session.close()
        return results

    # Получает список продуктов определенного лимита, начиная с какой либо строки,
    # переданной через пременную offset, и если передан seller, то от определенного производителя
    def get_products(self, limit, offset, seller):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            results = session.query(Product).limit(limit).offset(offset).all()
        except:
            JSONResponse(status_code=404, content={'message': "Ошибка"})

        if seller:
            for element in results[:]:
                if element.seller != seller:
                    results.remove(element)

        session.close()
        return results

    # Получает список заказов определенного лимита, начиная с какой либо строки,
    # переданной через пременную offset, и если передан user_id, то от определенного пользователя
    def get_orders(self, limit, offset, user_id):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            results = session.query(Order).limit(limit).offset(offset).all()
        except:
            JSONResponse(status_code=404, content={'message': "Ошибка"})

        if user_id:
            for element in results[:]:
                if element.user_id != user_id:
                    results.remove(element)

        session.close()
        return results

    # Добавляет юзера в базу данных, передавая имя пользователя, номер телефона, его адрес
    # и электронную почту
    def add_user(self, username, phone, address, email):
        Session = sessionmaker(self.engine)
        session = Session()

        user = User(username=username, phone=phone, address=address, email=email)
        session.add(user)
        session.commit()
        session.close()
        return user

    # Добавляет продукт в базу данных, передавая название, продавца
    # и стоимость
    def add_product(self, name, seller, price):
        Session = sessionmaker(self.engine)
        session = Session()

        product = Product(name=name, seller=seller, price=price)
        session.add(product)
        session.commit()
        session.close()
        return product

    # Добавляет заказ в базу данных, передавая id пользовател, id продукта,
    # который он заказал, и количество
    def add_order(self, user_id, product_id, count):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            user = session.query(User).filter(User.id == user_id).first()
            product = session.query(Product).filter(Product.id == product_id).first()
        except:
            JSONResponse(status_code=404, content={"message": 'Ошибка'})

        if user is None:
            JSONResponse(status_code=404, content={"message": 'Пользователь не найден'})

        if product is None:
            JSONResponse(status_code=404, content={"message": 'Продукт не найден'})

        order = Order(user=user, product=product, count=count)
        session.add(order)
        session.commit()
        session.close()
        return order

    # Изменяет имя пользователя, номер телефона, его адрес и электронную почту по переданному id
    # и возвращает ошибку, если пользователь не найден
    def update_user(self, user_id, username, phone, address, email):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            user = session.query(User).filter(User.id == user_id).first()
        except:
            JSONResponse(status_code=404, content={"message": 'Ошибка'})

        if user is None:
            JSONResponse(status_code=404, content={"message": 'Пользователь не найден'})

        user.username = username
        user.phone = phone
        user.address = address
        user.email = email
        session.commit()
        session.refresh(user)
        return user

    # Изменяет название, продавца и стоимость по переданному и id возвращает ошибку,
    # если продукт не найден
    def update_product(self, product_id, name, seller, price):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            product = session.query(Product).filter(Product.id == product_id).first()
        except:
            JSONResponse(status_code=404, content={"message": 'Ошибка'})

        if product is None:
            JSONResponse(status_code=404, content={"message": 'Продукт не найден'})

        product.name = name
        product.seller = seller
        product.price = price
        session.commit()
        session.refresh(product)
        return product

    # Изменяет id пользовател, id продукта и количество по переданному id
    # и возвращает ошибку, если пользователь не найден
    def update_order(self, order_id, user_id, product_id, count):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            order = session.query(Order).filter(Order.id == order_id).first()
            user = session.query(User).filter(User.id == user_id).first()
            product = session.query(Product).filter(Product.id == product_id).first()
        except:
            return JSONResponse(status_code=404, content={"message": 'Ошибка'})

        if order is None:
            return JSONResponse(status_code=404, content={"message": 'Заказ не найден'})

        if user is None:
            JSONResponse(status_code=404, content={"message": 'Пользователь не найден'})

        if product is None:
            JSONResponse(status_code=404, content={"message": 'Продукт не найден'})

        order.user = user
        order.product = product
        order.count = count
        session.commit()
        session.refresh(order)
        return order

    # Удаляет пользователя из базы данных по его id, если его нет возвращает ошибку
    def delete_user(self, user_id):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            user = session.query(User).filter(User.id == user_id).first()
        except:
            return JSONResponse(status_code=404, content={"message": 'Ошибка'})

        if user is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})

        session.delete(user)
        session.commit()

        session.close()
        return user

    # Удаляет продукт из базы данных по его id, если его нет возвращает ошибку
    def delete_product(self, product_id):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            product = session.query(Product).filter(Product.id == product_id).first()
        except:
            return JSONResponse(status_code=404, content={"message": "Ошибка"})

        if product is None:
            JSONResponse(status_code=404, content={"message": 'Продукт не найден'})

        session.delete(product)
        session.commit()
        session.close()

        return product

    # Удаляет заказ из базы данных по его id, если его нет возвращает ошибку
    def delete_order(self, order_id):
        Session = sessionmaker(self.engine)
        session = Session()

        try:
            order = session.query(Order).filter(Order.id == order_id).first()
        except:
            return JSONResponse(status_code=404, content={"message": "Ошибка"})

        if order is None:
            JSONResponse(status_code=404, content={"message": 'Заказ не найден'})

        session.delete(order)
        session.commit()
        session.close()

        return order
