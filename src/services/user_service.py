from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.database.database_utils import add, get_by_id
from src.models.models import User
from src.services.password_service import hash_and_spice_password


def check_password(db: Session, id: str, password: str) -> Optional[HTTPException]:
    # get the user from the database
    user = get_by_id(db, User, id)
    if isinstance(user, HTTPException):
        return user

    # check the password
    hashed_password, _ = hash_and_spice_password(password, str(user.salt))
    if hashed_password != str(user.password):
        return HTTPException(status_code=401, detail="Password is incorrect")


def add_user_with_pw(db: Session, hashed_password: str, salt: str) -> User:
    user = User(hashed_password=hashed_password, salt=salt, username="Gopher", email="", firstname="", lastname="")
    add(db, user)
    return user
