from database.base import Base
import sqlalchemy
import sqlalchemy as sq


class VkUser(Base):
    __tablename__ = 'vk_user'

    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    profile_link = sq.Column(sq.String)