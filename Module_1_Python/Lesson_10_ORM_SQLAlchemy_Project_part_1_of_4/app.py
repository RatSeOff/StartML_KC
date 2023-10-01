from fastapi import FastAPI, HTTPException
from database import SessionLocal
from table_user import User
from table_post import Post
from table_feed import Feed
from schema import UserGet, PostGet, FeedGet
from sqlalchemy import desc
from sqlalchemy.sql.functions import count
from typing import List

app = FastAPI()


@app.get('/user/{id}', response_model=UserGet)
def get_user_by_id(id: int):
    with SessionLocal() as session:
        result = session \
            .query(User) \
            .filter(User.id == id) \
            .first()
        if result:
            return result
        raise HTTPException(404, 'User not found')


@app.get('/user/{id}/feed', response_model=List[FeedGet])
def get_feed_by_user_id(id: int, limit: int = 10):
    with SessionLocal() as session:
        result = session \
            .query(Feed) \
            .filter(Feed.user_id == id) \
            .order_by(desc(Feed.time)) \
            .limit(limit) \
            .all()
        if result:
            return result
        raise HTTPException(200, [])


@app.get('/post/{id}', response_model=PostGet)
def get_post_by_id(id: int):
    with SessionLocal() as session:
        result = session \
            .query(Post) \
            .filter(Post.id == id) \
            .first()
        if result:
            return result
        raise HTTPException(404, 'Post not found')


@app.get('/post/{id}/feed', response_model=List[FeedGet])
def get_feed_by_post_id(id: int, limit: int = 10):
    with SessionLocal() as session:
        result = session \
            .query(Feed) \
            .filter(Feed.post_id == id) \
            .order_by(desc(Feed.time)) \
            .limit(limit) \
            .all()
        if result:
            return result
        raise HTTPException(200, [])


@app.get('/post/recommendations/', response_model=List[PostGet])
def get_recommendations(id: int = 0, limit: int = 10):
    with SessionLocal() as session:
        result = session \
            .query(Post) \
            .select_from(Feed) \
            .filter(Feed.action == "like") \
            .join(Post) \
            .group_by(Post.id) \
            .order_by(desc(count(Post.id))) \
            .limit(limit) \
            .all()
        return result
