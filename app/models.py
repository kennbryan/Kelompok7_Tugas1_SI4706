from sqlalchemy import Column, Integer, String
from app.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    name = Column(String(256), nullable=True)

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    price = Column(Integer, nullable=False)