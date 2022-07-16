from sqlalchemy import Column
from . database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, primary_key = False, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, default = True)
