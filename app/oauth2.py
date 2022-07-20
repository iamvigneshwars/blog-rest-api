from datetime import timedelta, datetime
from jose import JWTError, jwt

SECRET_KEY = "31117f148cf10a70a8fbbdd36f32727066cb8645ecbdeada3e4ae986f53fdcca"
ALGORITHM = "HS256"
TOKEN_EXPIRE = 30

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes = TOKEN_EXPIRE)
    to_encode.update({"exp": expire})

    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return  encoded_token