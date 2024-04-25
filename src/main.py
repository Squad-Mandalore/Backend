from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.controllers import (
    athlete_controller,
    auth_controller,
    category_controller,
    completes_controller,
    csv_controller,
    exercise_controller,
    log_controller,
    rule_controller,
    trainer_controller,
    admin_controller
)
from src.database.database_setup import init_db
from src.middleware.cors import add_cors_middleware
from src.services.log_service import clear_error_log

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    await clear_error_log()
    yield

app = FastAPI(lifespan=lifespan)

add_cors_middleware(app)
app.include_router(admin_controller.router)
app.include_router(trainer_controller.router)
app.include_router(athlete_controller.router)
app.include_router(completes_controller.router)
app.include_router(category_controller.router)
app.include_router(exercise_controller.router)
app.include_router(rule_controller.router)
app.include_router(auth_controller.router)
app.include_router(csv_controller.router)
app.include_router(log_controller.router)
