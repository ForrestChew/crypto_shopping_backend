from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from .config import settings
from .database import conn, create_tables

app = FastAPI()

create_tables()


@app.get("/")
def root():
    return "Hello"
