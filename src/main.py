import sqlite3
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

with sqlite3.connect("db/test.db") as conn:
    cur = conn.cursor()
    # Insert Queries here

print("This is the way")