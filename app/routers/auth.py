from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schemas, utils, models

router = APIRouter(tags = ["Authentication"])

@router.post('/login')
def login(user_cred : schemas.Login,db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_cred.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid Cred")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid Cred")

    # print(user.password)

    return user_cred
