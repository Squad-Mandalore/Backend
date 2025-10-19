from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.controllers import admin_controller
from src.controllers import athlete_controller
from src.controllers import auth_controller
from src.controllers import category_controller
from src.controllers import certificate_controller
from src.controllers import completes_controller
from src.controllers import csv_controller
from src.controllers import exercise_controller
from src.controllers import log_controller
from src.controllers import rule_controller
from src.controllers import trainer_controller
from src.database.database_setup import init_db
from src.middleware.cors import add_cors_middleware
from src.services.logger_service import clear_error_log


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
app.include_router(certificate_controller.router)
app.include_router(completes_controller.router)
app.include_router(category_controller.router)
app.include_router(exercise_controller.router)
app.include_router(rule_controller.router)
app.include_router(auth_controller.router)
app.include_router(csv_controller.router)
app.include_router(log_controller.router)
