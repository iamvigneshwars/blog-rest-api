from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas, utils  
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List


models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def root():
    return {"Info": "This is an blog post CRUD API that allows users to create, update, and delete a post"}

# Get all the posts
@app.get("/posts", response_model = List[schemas.PostResponse])
def root(db : Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return posts 

# Create a new post in a database
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create(post : schemas.PostCreate, db: Session = Depends(get_db)):
   
    new_post = models.Post(**post.dict())
    
    # Add the new post content to the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post 

# Get a post with specific ID
@app.get("/posts/{id}", response_model = schemas.PostResponse)
def get_post(id: int, db : Session = Depends(get_db)):

    post = db.query(models.Post).where(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
      
    return post 


# Delete a post from the database
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):

    post = db.query(models.Post).where(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id: {id} was not found')

    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


# Update a post in the database
@app.put("/posts/{id}", response_model = schemas.PostResponse)
def update_post(id : int, updated_post : schemas.PostCreate, db : Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id: {id} was not found')

    post_query.update(updated_post.dict())
    db.commit()

    return post_query.first()


# User Registration
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):

    # Hash the password
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    # Add the new post content to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 


# Get all the users
# @app.get("/users", response_model = List[schemas.UserCreate])
@app.get("/users" ,response_model = List[schemas.UserAll])
def get_users(db : Session = Depends(get_db)):

    users= db.query(models.User).all()

    return users


# Get a Specific user based on their id
@app.get('/users/{id}',response_model= schemas.UserOut)
def get_user(db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id)
    user = user.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with id: {id} was not found')

    return user