from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password : str):
    return pwd_context.hash(password)

def verify(credential : str, password : str):
    # return password == hash(credential)
    return pwd_context.verify(credential, password)
