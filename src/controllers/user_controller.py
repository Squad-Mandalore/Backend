from fastapi import APIRouter, status
from src.database.database_utils import get_all

from src.models.user_model import User
from src.schemas.password_schema import PasswordSchema
from src.schemas.user_schema import UserSchema
from src.services.password_service import hash_and_spice_password
from src.services.password_validation_service import validate_password
from src.services.user_service import check_password, add_user_with_pw

router = APIRouter(
    # routing prefix
    prefix="/users",
    # documentation tag
    tags=["users"],
    # default response
    responses={404: {"route": "Not found"}}
)


@router.get("/all", response_model=list[UserSchema])
async def get_all_entries() -> list[User]:
    users = get_all(User)
    return users


@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def post_password(password_schema: PasswordSchema) -> User:
    password = password_schema.password
    validate_password(password)

    hashed_password, salt = hash_and_spice_password(password)
    user = add_user_with_pw(hashed_password, salt)
    return user


@router.post("/login", status_code=status.HTTP_202_ACCEPTED) # will probably replaced with verify user and then 2FA and jwt token
async def post_login(user_schema: UserSchema) -> None:
    id = user_schema.id
    password = user_schema.password
    check_password(id, password)
