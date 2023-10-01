from fastapi import FastAPI, HTTPException, Depends
import datetime as dt
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import json

app = FastAPI()


# @app.get('/')
# def root():
#     return 'hello, world'

@app.get('/')
def sum(a: int, b: int):
    return a + b


@app.get('/sum_date')
def sum_date(current_date: dt.date, offset: int):
    return current_date + dt.timedelta(days=offset)


class User(BaseModel):
    name: str
    surname: str
    age: int
    registration_date: dt.date


@app.post('/user/validate')
def validate(User: User):
    return f'Will add user: {User.name} {User.surname} with age {User.age}'


def get_db():
    link = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
    curs_type = RealDictCursor
    conn = psycopg2.connect(link, cursor_factory=curs_type)
    return conn


@app.get('/user/{id}')
def get_gen_age_cit(id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            f'''  
            SELECT gender, age, city
            FROM "user"
            WHERE id={id}
            '''
        )
        result = cursor.fetchone()
        if not result:
            raise HTTPException(404, 'user not found')
        else:
            return result


class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config():
        orm_mode = True


@app.get('/post/{id}', response_model=PostResponse)
def get_info(id: int, db=Depends(get_db)) -> PostResponse:
    with db.cursor() as cursor:
        cursor.execute(
            f'''
            SELECT id, text, topic
            FROM post
            WHERE id={id}
            '''
        )
        result = cursor.fetchone()
        if not result:
            raise HTTPException(404, 'post not found')
        else:
            return PostResponse(**result)
