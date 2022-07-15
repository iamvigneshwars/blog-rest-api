from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

from regex import F


app = FastAPI()

class Post(BaseModel):
    title : str
    content: str
    published : bool = True
    rating : Optional[int] = None

my_posts = [
    {"title" : "TITLE 1", "content" : "This is the first post", "id" : 1},

    {"title" : "TITLE 2", "content" : "I like pizza", "id" : 2}
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def root():
    # return {"message": "This is the post page"}
    print(my_posts[0]["id"])
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create(post : Post):
    # print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


def find_post(id):
    for dict in my_posts:
        print(dict["id"])
        if (dict["id"] == (id)):
            return dict

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    in_post = find_post(int(id))
    if not in_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"messgage" : f"Post with ID {id} not found"}
    # return {"post_detail" : f"here is post {id}"}
    return {"post" : in_post}

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

