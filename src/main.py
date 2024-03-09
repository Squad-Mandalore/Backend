from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.controllers import (
    athlete_controller,
    log_controller,
    password_controller,
    user_controller,
    auth_controller
)
from src.database.database_setup import init_db
from src.middleware.cors import add_cors_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

add_cors_middleware(app)
app.include_router(password_controller.router)
app.include_router(user_controller.router)
app.include_router(athlete_controller.router)
app.include_router(log_controller.router)
app.include_router(auth_controller.router)
