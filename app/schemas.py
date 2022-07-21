from typing import Optional
from numpy import std
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.database import Base


class PostBase(BaseModel):
    title : str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email : EmailStr
    password : str


class Login(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None