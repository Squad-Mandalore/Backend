from src.database.database_setup import init_db
from fastapi import FastAPI
from src.controllers import password_controller, user_controller
from src.logger.logger import logger

init_db()

logger.info("Starting FastAPI")

app = FastAPI()

app.include_router(password_controller.router)
app.include_router(user_controller.router)
