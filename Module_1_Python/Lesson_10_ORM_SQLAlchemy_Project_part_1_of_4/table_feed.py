from database import Base
from sqlalchemy import ForeignKey, Integer, Column, String, DateTime
from sqlalchemy.orm import relationship
from table_post import Post
from table_user import User


class Feed(Base):
    __tablename__ = "feed_action"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    user = relationship(User, lazy='subquery')
    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)
    post = relationship(Post, lazy='subquery')
    action = Column(String)
    time = Column(DateTime)
