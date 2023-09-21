from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, ForeignKey
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
# from tables import Order, User, Product

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

    # def append(self, user_list, product_list, order_list):
    #     self.create_database()
    #     Session = sessionmaker(self.engine)
    #     session = Session()
    #
    #
    #
    #     session.commit()
    #     session.close()
