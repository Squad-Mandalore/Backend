from src.schemas.user_schema import UserSchema
from src.services.user_service import check_password
from ..database.database_utils import get_all
from fastapi import FastAPI, APIRouter, HTTPException

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
    user = password_service(password)
    return user

@router.post("/login")
async def post_login(string: UserSchema):
    id = string.id
    password = string.password
    result = check_password(id, password)

    if result:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password or user")
