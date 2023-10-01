from database import Base
from sqlalchemy import Integer, String, Column


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)
