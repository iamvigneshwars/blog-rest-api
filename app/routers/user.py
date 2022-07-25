from multiprocessing.sharedctypes import synchronized
from unittest import expectedFailure
from .. import models, schemas, utils
from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List


router = APIRouter(prefix = "/users", tags=['Users'])
 
# User Registration
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db)):


    # Check if the user already exists and return conflict status
    already_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if already_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= "User already exists!")

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
@router.get("/", response_model = List[schemas.UserOut])
def get_users(db : Session = Depends(get_db)):

    users= db.query(models.User).all()

    return users


# Get a Specific user based on their id
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User with id: {id} was not found')

    return user

# Delete a User
@router.delete("/delete/{id}")
def delete_user(id : int, db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")

    user.delete(synchronize_session = False)
    db.commit()
    return Response(status_code= status.HTTP_404_NOT_FOUND)