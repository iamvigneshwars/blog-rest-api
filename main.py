from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def root():
    return {"message": "This is the post page"}

@app.post("/create")
def create(payload : dict = Body(...)):
    print(payload)
    return {"message": "Created post"}