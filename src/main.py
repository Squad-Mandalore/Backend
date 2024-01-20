from .database.database_setup import Session, init_db
from fastapi import FastAPI


app = FastAPI()


init_db()

session = Session()
