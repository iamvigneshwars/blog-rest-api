from .. import models, schemas, utils
from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()

# Get all the posts
@router.get("/posts", response_model = List[schemas.PostResponse])
def root(db : Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return posts 

# Create a new post in a database
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create(post : schemas.PostCreate, db: Session = Depends(get_db)):
   
    new_post = models.Post(**post.dict())
    
    # Add the new post content to the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post 

# Get a post with specific ID
@router.get("/posts/{id}", response_model = schemas.PostResponse)
def get_post(id: int, db : Session = Depends(get_db)):

    post = db.query(models.Post).where(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
      
    return post 


# Delete a post from the database
@router.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):

    post = db.query(models.Post).where(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id: {id} was not found')

    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


# Update a post in the database
@router.put("/posts/{id}", response_model = schemas.PostResponse)
def update_post(id : int, updated_post : schemas.PostCreate, db : Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id: {id} was not found')

    post_query.update(updated_post.dict())
    db.commit()

    return post_query.first()