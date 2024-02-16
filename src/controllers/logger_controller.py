from fastapi import APIRouter
from starlette.responses import FileResponse


router = APIRouter(
    # routing prefix
    prefix="/logger",
    # documentation tag
    tags=["logger"],
    # default response
    responses={404: {"route": "Not found"}}
)

@router.get("/error.log", response_class=FileResponse)
async def read_debug_log():
    return "error.log"
