from sqlalchemy import Column, Integer, String, MetaData

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()

class Question(Base):
    __tablename__ = "questions"
    
    metadata
    
    pk = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer)
    question = Column(String)
    answer = Column(String)
    created_at = Column(String)
    