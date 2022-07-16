from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

class Post(BaseModel):
    title : str
    content: str
    published : bool = True
    # rating : Optional[int] = None

my_posts = [
    {"title" : "TITLE 1", "content" : "This is the first post", "id" : 1},

    {"title" : "TITLE 2", "content" : "I like pizza", "id" : 2}
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Get all the posts
@app.get("/posts")
def root(db : Session = Depends(get_db)):
    # return {"message": "This is the post page"}
    posts = db.query(models.Post).all()
    # print(my_posts[0]["id"])
    return {"data": posts}

# Create a new post in a database
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create(post : Post, db: Session = Depends(get_db)):
   
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


# # Get the post for sepcific id
# def find_post(id : int, db : Session = Depends(get_db)):

#     posts = db.query(models.Post).all()
#     print(posts)


@app.get("/posts/{id}")
def get_post(id: int, db : Session = Depends(get_db)):

    post = db.query(models.Post).where(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"messgage" : f"Post with ID {id} not found"}
    # return {"post_detail" : f"here is post {id}"}
    return {"post" : post}

def find_index_post(id):
    for i , p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find the index in the array that has the required ID
    index = find_index_post(id)
    if (not index):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id: {id} was not found')
    my_posts.pop(index)

    return Response(status_code = status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}")
def udpate_post(id : int, post : Post):
    print(post)

    index = find_index_post(id)
    if (not index):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id: {id} was not found')

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {'data' : post_dict}
