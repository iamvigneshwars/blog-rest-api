from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from . import models, schemas, utils  
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from .routers import post, user

router = APIRouter()

models.Base.metadata.create_all(bind = engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"Info": "This is an blog post CRUD API that allows users to create, update, and delete a post"}
