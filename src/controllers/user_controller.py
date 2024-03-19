from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_all, get_db
from src.models.models import Base, User
from src.schemas.user_schema import UserResponseSchema
from src.services.password_service import hash_and_spice_password, validate_password

router = APIRouter(
    # routing prefix
    prefix="/users",
    # documentation tag
    tags=["users"],
    # default response
    #responses={404: {"route": "Not found"}}
)

'''
@router.get("/all", response_model=list[UserSchema])
async def get_all_entries(db: Session = Depends(get_db)) -> list[Base]:
    users = get_all(db, User)
    if isinstance(users, HTTPException):
        raise users
    return users


@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def post_password(password_schema: PasswordSchema, db: Session = Depends(get_db)) -> User:
    password = password_schema.password
    validated = validate_password(password)
    if isinstance(validated, HTTPException):
        raise validated

    hashed_password, salt = hash_and_spice_password(password)
    user = add_user_with_pw(db, hashed_password, salt)
    return user


@router.post("/login", status_code=status.HTTP_202_ACCEPTED) # will probably replaced with verify user and then 2FA and jwt token
async def post_login(user_schema: UserSchema, db: Session = Depends(get_db)) -> None:
    id = user_schema.id
    password = user_schema.password

    checked = check_password(db, id, password)
    if isinstance(checked, HTTPException):
        raise checked
'''
