from fastapi import Response, status

from src.database.database_utils import add, get_by_id
from src.models.user_model import User
from src.services.password_service import hash_and_spice_password


def check_password(id: str, password: str) -> Response:
    # get the user from the database

    user = get_by_id(User, id)

    if not user:
        return Response(content="User not found", status_code=status.HTTP_404_NOT_FOUND)

    hashed_password, _ = hash_and_spice_password(password, str(user.salt))

    if hashed_password == str(user.password):
        return Response(content="Password is correct", status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(content="Password is wrong", status_code=status.HTTP_401_UNAUTHORIZED)


def add_user_with_pw(hashed_password: str, salt: str) -> User:
    user = User(hashed_password, salt)
    add(user)
    return user
