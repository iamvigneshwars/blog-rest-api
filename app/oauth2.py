from datetime import timedelta, datetime
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from regex import P
from . import schemas
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "31117f148cf10a70a8fbbdd36f32727066cb8645ecbdeada3e4ae986f53fdcca"
ALGORITHM = "HS256"
TOKEN_EXPIRE = 30

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = TOKEN_EXPIRE)
    to_encode.update({"exp": expire})

    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return  encoded_token


def verify_token(token : str, credential_exception):

    try:
        payload = jwt.decode(token , SECRET_KEY, algorithms=ALGORITHM)

        print(payload)
        id = payload.get("user_id")
        print(id)

        if id is None:
            raise credential_exception
        
        token =schemas.TokenData(id = id)
    except JWTError:
        raise credential_exception
    
    return token

def get_current_user(token :str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = "Could not validate the credentials", headers = {"WWW-Authenticate" : "Bearer"})

    return verify_token(token, credentials_exception)