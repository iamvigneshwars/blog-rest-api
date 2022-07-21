from datetime import timedelta, datetime
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from . import schemas, models, database
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRE = settings.access_token_expire_minutes

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = TOKEN_EXPIRE)
    to_encode.update({"exp": expire})

    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return  encoded_token


def verify_token(token : str, credential_exception):

    try:
        payload = jwt.decode(token , SECRET_KEY, algorithms=ALGORITHM)

        id = payload.get("user_id")
        if id is None:
            raise credential_exception
        
        token =schemas.TokenData(id = id)
    except JWTError:
        raise credential_exception
    
    return token

def get_current_user(token :str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = "Could not validate the credentials", headers = {"WWW-Authenticate" : "Bearer"})

    token = verify_token(token, credentials_exception)

    current_user = db.query(models.User).filter(models.User.id == token.id).first()

    return current_user 