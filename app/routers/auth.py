from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database, schemas, utils, models, oauth2

router = APIRouter(tags = ["Authentication"])

@router.post('/login')
def login(credential : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid Cred")

    # print(user.password)

    if not utils.verify(credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid Cred")


    token = oauth2.create_token(data = {"user_email" : user.email})

    return {"token" : token, "token_type" : "bearer"}
