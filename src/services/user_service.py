from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.database.database_utils import get_by_id
from src.models.models import User
from src.services.password_service import hash_and_spice_password


def check_password(id: str, password: str, db: Session) -> Optional[HTTPException]:
    # get the user from the database
    user = get_by_id(User, id, db)
    if isinstance(user, HTTPException):
        return user

    # check the password
    hashed_password, _ = hash_and_spice_password(password, str(user.salt))
    if hashed_password != str(user.password):
        return HTTPException(status_code=401, detail="Password is incorrect")
