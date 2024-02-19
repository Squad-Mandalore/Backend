from fastapi import APIRouter, status
from starlette.responses import FileResponse
from src.schemas.log_schema import LogSchema

from src.logger.logger import logger


router = APIRouter(
    # routing prefix
    prefix="/log",
    # documentation tag
    tags=["log"],
    # default response
    responses={404: {"route": "Not found"}}
)

@router.get("/error.log", response_class=FileResponse)
async def read_debug_log() -> FileResponse:
    return FileResponse("error.log")


@router.post("/debug", status_code=status.HTTP_200_OK)
async def debug(message: LogSchema):
    logger.debug(message)


@router.post("/info", status_code=status.HTTP_200_OK)
async def info(message: LogSchema):
    logger.info(message)


@router.post("/warning", status_code=status.HTTP_200_OK)
async def warning(message: LogSchema):
    logger.warning(message)


@router.post("/critical", status_code=status.HTTP_200_OK)
async def critical(message: LogSchema):
    logger.critical(message)


@router.post("/error", status_code=status.HTTP_200_OK)
async def error(message: LogSchema):
    logger.error(message)