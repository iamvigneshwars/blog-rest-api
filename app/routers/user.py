from .. import models, schemas, utils
from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List


router = APIRouter()
 
# User Registration
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
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
# @router.get("/users", response_model = List[schemas.UserCreate])
@router.get("/users" ,response_model = List[schemas.UserOut])
def get_users(db : Session = Depends(get_db)):

    users= db.query(models.User).all()

    return users


# Get a Specific user based on their id
@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with id: {id} was not found')

    return user
