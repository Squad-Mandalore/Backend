import os

from fastapi import APIRouter, HTTPException, status
from starlette.responses import FileResponse

from src.logger.logger import frontend_logger
from src.schemas.log_schema import LogSchema
from src.services.logger_service import error_log_path

router = APIRouter(
    # routing prefix
    prefix='/log',
    # documentation tag
    tags=['log'],
    # default response
    # responses={404: {"route": "Not found"}}
)


@router.get('/error.log', response_class=FileResponse, status_code=status.HTTP_200_OK)
async def read_error_log() -> FileResponse:
    if not os.path.exists(f'{error_log_path}'):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Log file not found'
        )

    return FileResponse(f'{error_log_path}')


@router.post('/debug', status_code=status.HTTP_200_OK)
async def debug(message: LogSchema):
    frontend_logger.debug(message.message)


@router.post('/info', status_code=status.HTTP_200_OK)
async def info(message: LogSchema):
    frontend_logger.info(message.message)


@router.post('/warning', status_code=status.HTTP_200_OK)
async def warning(message: LogSchema):
    frontend_logger.warning(message.message)


@router.post('/critical', status_code=status.HTTP_200_OK)
async def critical(message: LogSchema):
    frontend_logger.critical(message.message)


@router.post('/error', status_code=status.HTTP_200_OK)
async def error(message: LogSchema):
    frontend_logger.error(message.message)
