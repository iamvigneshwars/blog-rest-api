from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Post(BaseModel):
    title : str
    content: str
    published : bool = True
    rating : Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def root():
    return {"message": "This is the post page"}

@app.post("/create")
def create(post : Post):
    print(post.dict())
    return {"message": "Created post"}