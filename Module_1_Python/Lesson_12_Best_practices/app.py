from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import yaml

if __name__=="__main__":
    load_dotenv()
    os.system("uvicorn app:app --reload")

app = FastAPI()

def config():
    with open("params.yaml", 'r') as f:
        return yaml.safe_load(f)

def get_db():
    with psycopg2.connect(
        user=os.environ["USER"],
        password=os.environ["PASSWORD"],
        host=os.environ["HOST"],
        port=os.environ["PORT"],
        database=os.environ["DATABASE"],
    ) as conn:
        return conn

@app.get("/user")
def get_user(limit=10, db=Depends(get_db)):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT *
            FROM "user"
            LIMIT %(limit)s
            """,
            {"limit": limit}
        )
        return cursor.fetchall()

@app.get("/user/feed")
def get_user_feed (user_id: int, limit: int = 10, db = Depends(get_db), config: dict = Depends(config)):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM feed_action
            WHERE user_id = %(user_id)s
                AND time >= %(FEED_START_DATE)s
            LIMIT %(limit)s
            """,
            {"user_id": user_id, "limit": limit, "FEED_START_DATE": config["FEED_START_DATE"]}
        )
        return cursor.fetchall()


