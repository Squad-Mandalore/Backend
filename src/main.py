from .database.database_setup import init_db
from fastapi import FastAPI
from .controllers import password_controller, user_controller

init_db()

app = FastAPI()

app.include_router(password_controller.router)
app.include_router(user_controller.router)
