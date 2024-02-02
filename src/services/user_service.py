from fastapi import HTTPException

from src.database.database_utils import add, get_by_id
from src.models.user_model import User
from src.services.password_service import hash_and_spice_password


def check_password(id: str, password: str) -> None:
    # get the user from the database
    user = get_by_id(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # check the password
    hashed_password, _ = hash_and_spice_password(password, str(user.salt))
    if hashed_password != str(user.password):
        raise HTTPException(status_code=401, detail="Password is incorrect")


def add_user_with_pw(hashed_password: str, salt: str) -> User:
    user = User(hashed_password, salt)
    add(user)
    return user
