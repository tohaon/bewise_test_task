from sqlalchemy import Column, Integer, String, MetaData, LargeBinary

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()

class Audio(Base):
    __tablename__ = "audios"
    
    metadata
    
    pk = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String)
    user_id = Column(String)
    audio = Column(LargeBinary)