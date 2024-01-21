from fastapi import APIRouter, status
from src.database.database_utils import get_all

from src.models.user_model import User
from src.schemas.password_schema import PasswordSchema
from src.schemas.user_schema import UserSchema
from src.services.password_service import password_service
from src.services.user_service import check_password

router = APIRouter()


@router.get("/allUser")
async def get_all_entries():
    return get_all(User)


@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def post_password(password_schema: PasswordSchema):
    password = password_schema.password
    user = password_service(password)
    return user


@router.post("/login")
async def post_login(user_schema: UserSchema):
    id = user_schema.id
    password = user_schema.password
    result = check_password(id, password)
    return result


# which one is better design wise
# @router.post("/login")
# async def post_login(user_schema: UserSchema):
#     result = check_password(user_schema)
#     return result
