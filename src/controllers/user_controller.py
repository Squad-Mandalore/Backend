from typing import Optional
from fastapi import APIRouter, Response, status
from src.database.database_utils import get_all

from src.models.user_model import User
from src.schemas.password_schema import PasswordSchema
from src.schemas.user_schema import UserSchema
from src.services.password_service import hash_and_spice_password
from src.services.user_service import check_password, add_user_with_pw

router = APIRouter(
    # routing prefix
    prefix="/users",
    # documentation tag
    tags=["users"],
    # default response
    responses={404: {"route": "Not found"}}
)


@router.get("/all")
async def get_all_entries() -> Optional[list[User]]:
    return get_all(User)


@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def post_password(password_schema: PasswordSchema) -> User:
    password = password_schema.password
    hashed_password, salt = hash_and_spice_password(password)
    user = add_user_with_pw(hashed_password, salt)
    return user


@router.post("/login") # will probably replaced with verify user and then 2FA
async def post_login(user_schema: UserSchema) -> Response:
    id = user_schema.id
    password = user_schema.password
    result = check_password(id, password)
    return result


# which one is better design wise
# @router.post("/login")
# async def post_login(user_schema: UserSchema):
#     result = check_password(user_schema)
#     return result
