from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schemas, utils, models

router = APIRouter(tags = ["Authentication"])

@router.post('/login')
def login(credential : schemas.Login,db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == credential.email).first()

    print(user.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid Cred")

    # print(user.password)

    if not utils.verify(credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Invalid Cred")



    return {"token" : "example token"}
