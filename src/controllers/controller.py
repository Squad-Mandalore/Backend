from ..database.database_utils import get_all
from fastapi import FastAPI, APIRouter

from ..models.user_model import User
from ..schemas.password_schema import PasswordSchema
from ..services.password_service import password_service

router = APIRouter()


def router_func(app: FastAPI):
    app.include_router(router)


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.get("/allUser")
async def get_all_entries():
    return get_all(User)


@router.post("/password")
async def post_password(password_schema: PasswordSchema):
    password = password_schema.password
    password_service(password)
    return "password added"
