from fastapi import Response, status

from src.database.database_setup import session
from src.database.database_utils import add
from src.models.user_model import User
from src.services.password_service import hash_password, pepper_password, salt_password


def check_password(id, password):
    # get the user from the database
    user = session.query(User).filter(User.id == id).first()

    if not user:
        return Response(content="User not found", status_code=status.HTTP_404_NOT_FOUND)

    salted_password, _ = salt_password(password, user.salt)
    peppered_password = pepper_password(salted_password)
    hashed_password = hash_password(peppered_password)

    if hashed_password == user.password:
        return Response(content="Password is correct", status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(content="Password is wrong", status_code=status.HTTP_401_UNAUTHORIZED)


def add_user_with_pw(hashed_password, salt):
    user = User(hashed_password, salt)
    add(user)
    return user
