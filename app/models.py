from .database import Base
from sqlalchemy import Column, Integer , String

class blog(Base):

    __tablename__= 'blogs'

    ID = Column(Integer, primary_key=True, index=True)
    title= Column(String) 
    body= Column(String) 

class user(Base):

    __tablename__= 'users'

    ID = Column(Integer, primary_key=True, index=True)
    name= Column(String)
    email= Column(String)
    password= Column(String)

