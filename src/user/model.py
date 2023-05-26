from sqlalchemy import Column, Integer, String, MetaData

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()

class User(Base):
    __tablename__ = "users"
    
    metadata
    
    pk = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)
    user_id = Column(String)
    access_token = Column(String)
