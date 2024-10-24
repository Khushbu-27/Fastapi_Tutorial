from fastapi import FastAPI, Depends ,status, Response, HTTPException
from . import schemas, models
from .database import engine , SessionLocal
from sqlalchemy.orm import Session 
from typing_extensions import List
from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/app', status_code=201 , tags=['blog'])
def create(request: schemas.blogs, db: Session = Depends(get_db)):
    new_blog = models.blog(title= request.title, body= request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/app', response_model= List[schemas.Showblogs],tags=['blog'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.blog).all()
    return blogs


@app.get('/app/{id}', status_code=200, response_model= schemas.Showblogs, tags=['blog'])
def show(id,db: Session = Depends(get_db)):
    blogs = db.query(models.blog).filter(models.blog.ID == id).first()
    if not blogs:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':'blog not found'}
    return blogs

@app.delete('/blog/{id}', status_code= status.HTTP_204_NO_CONTENT, tags=['blog'])
def remove(id, db: Session = Depends(get_db)):
    blogs = db.query(models.blog).filter(models.blog.ID == id)

    if not blogs:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="blog not found")
    
    blogs.delete(synchronize_session=False)
    db.commit()
    return 'sucessfully deleted'


@app.put('/blog/{id}', status_code= status.HTTP_202_ACCEPTED, tags=['blog'])
def update_blog(id,request: schemas.blogs ,db: Session = Depends(get_db)):
    blogs = db.query(models.blog).filter(models.blog.ID == id)

    if not blogs:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="blog not found")
    
    blogs.update(request)
    db.commit()
    return 'updated sucessfully'

pwd_cxt = CryptContext(schemes = ["bcrypt"], deprecated= 'auto')

@app.post('/user', status_code= 201, tags=['users'])
def create_users(request: schemas.User, db: Session = Depends(get_db)):
    hasedPassword = pwd_cxt.hash(request.password)
    new_user= models.user(name= request.name , email = request.email, password= hasedPassword)
    db.add(new_user)
    db.commit()                 
    db.refresh(new_user)
    return new_user

