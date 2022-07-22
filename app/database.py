from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:vishallahsiv@localhost/blogpost-api'
# SQLALCHEMY_DATABASE_URL = "postgresql://ziryjyvvdjpfiz:bb9c02354b9fa723558fab35b6f45b67995c6d106f227a4be21a478d5701642b@ec2-54-87-179-4.compute-1.amazonaws.com:5432/dd8mtje67apreo"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()