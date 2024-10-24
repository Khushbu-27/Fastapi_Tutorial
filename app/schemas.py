from pydantic import BaseModel

class blogs(BaseModel):
    title: str
    body: str

class Showblogs(blogs):
    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str