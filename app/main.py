from fastapi import FastAPI, APIRouter
from . import models, utils  
from .database import engine
from .routers import post, user, auth
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Info": "This is an blog post REST API that allows users to create, update, and delete a post"}
