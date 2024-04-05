from fastapi import APIRouter

router = APIRouter(
    # routing prefix
    prefix="/trainers",
    # documentation tag
    tags=["trainers"],
    # default response
    #responses={404: {"route": "Not found"}},
)