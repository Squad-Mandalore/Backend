from .database.database_setup import init_db
from fastapi import FastAPI
from .controllers.controller import router_func


app = FastAPI()

init_db()
router_func(app)
