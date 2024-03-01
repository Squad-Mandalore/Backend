from fastapi import FastAPI

from src.controllers import (
    athlete_controller,
    log_controller,
    password_controller,
    user_controller,
)
from src.database.database_setup import init_db
from src.middleware.cors import add_cors_middleware

init_db()

app = FastAPI()

add_cors_middleware(app)
app.include_router(password_controller.router)
app.include_router(user_controller.router)
app.include_router(athlete_controller.router)
app.include_router(log_controller.router)
