from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from helpers import Base


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    password = Column(String(50), unique=True)
    nickname = Column(String(50), unique=True)
    c_time = Column(TIMESTAMP, default=datetime.now)

    def __init__(self, id=None, email=None, password=None, nickname=None, c_time=None):
        self.id = id
        self.email = email
        self.password = password
        self.nickname = nickname
        self.c_time = c_time

    #def __repr__(self):
    #    return ''

