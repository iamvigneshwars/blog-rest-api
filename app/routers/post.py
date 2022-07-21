from regex import P
from .. import models, schemas, utils, oauth2
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(prefix = '/posts', tags=["Posts"])

# Get all the posts
@router.get("/",  response_model = List[schemas.PostResponse])
def root(db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    print(current_user.email)

    posts = db.query(models.Post).all()

    return posts 

# Create a new post in a database
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create(post : schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
   
    new_post = models.Post(owner_id = current_user.id, **post.dict())
   # print("#######DEBUG########")
    # print(new_post.owner_id)
    
    # Add the new post content to the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post 

# Get a post with specific ID
@router.get("/{id}", response_model = schemas.PostResponse)
def get_post(id: int, db : Session = Depends(get_db)):

    post = db.query(models.Post).where(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
      
    return post 


# Delete a post from the database
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).where(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id: {id} was not found')

    if post.first().owner_id !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not autherized")

    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


# Update a post in the database
@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id : int, updated_post : schemas.PostCreate, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id: {id} was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not autherized")

    post_query.update(updated_post.dict())
    db.commit()

    return post_query.first()