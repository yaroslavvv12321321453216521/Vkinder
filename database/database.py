import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from database.base import Base
from database.models.vk_user import VkUser
from pprint import pprint


class Database:
    def __init__(self, database_link: str):
        engine = sqlalchemy.create_engine(database_link)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()
        self.db_session = session

    def add_vk_user(self, vk_user: VkUser):
        self.db_session.add(vk_user)
        self.db_session.commit()

    def is_user_exist(self, user_id: int):
        result = self.db_session.query(VkUser).filter(VkUser.id == user_id).all()
        return len(result) > 0
