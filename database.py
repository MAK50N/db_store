from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self):
        self.DatabaseUri = f"postgresql://postgres:1@localhost:5432/store"
        self.engine = create_engine(self.DatabaseUri)

    def create_database(self):
        if database_exists(self.DatabaseUri) is False:
            create_database(self.DatabaseUri)

        metadata = MetaData()
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
