import os
from fastapi import APIRouter, HTTPException, status
from starlette.responses import FileResponse
from src.schemas.log_schema import LogSchema

from src.logger.logger import frontend_logger


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
    if not os.path.exists("error.log"):
        raise HTTPException(status_code=404, detail="Log file not found")

    return FileResponse("error.log")


@router.post("/debug", status_code=status.HTTP_200_OK)
async def debug(message: LogSchema):
    frontend_logger.debug(message.message)


@router.post("/info", status_code=status.HTTP_200_OK)
async def info(message: LogSchema):
    frontend_logger.info(message.message)


@router.post("/warning", status_code=status.HTTP_200_OK)
async def warning(message: LogSchema):
    frontend_logger.warning(message.message)


@router.post("/critical", status_code=status.HTTP_200_OK)
async def critical(message: LogSchema):
    frontend_logger.critical(message.message)


@router.post("/error", status_code=status.HTTP_200_OK)
async def error(message: LogSchema):
    frontend_logger.error(message.message)
