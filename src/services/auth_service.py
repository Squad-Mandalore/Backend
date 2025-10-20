from datetime import datetime
from datetime import timedelta
from datetime import UTC
from os import getenv
from typing import cast

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import User
from src.schemas.auth_schema import Token
from src.services.password_service import verify_password


ALGORITHM = 'HS256'
JWT_KEY = getenv('JWT_KEY', 'test')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


def authenticate_user(username: str, password: str, db: Session) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(user, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


def get_tokens(form_data, db: Session) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    return get_user_tokens(user)


def get_refreshed_tokens(refresh_token: str, db: Session) -> Token:
    user = get_current_user(refresh_token, db)
    return get_user_tokens(user, refresh_token)


def get_user_tokens(user: User, refresh_token: str | None = None) -> Token:
    access_token = create_access_token(
        user.id, user.username, user.type, timedelta(minutes=15)
    )
    if not refresh_token:
        refresh_token = create_refresh_token(
            user.id, user.username, user.type, timedelta(minutes=10080)
        )

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type='bearer'
    )


def create_access_token(
    user_id: str, username: str, user_type: str, expires_delta: timedelta
) -> str:
    return create_token(user_id, username, user_type, expires_delta, 'access')


def create_refresh_token(
    user_id: str, username: str, user_type: str, expires_delta: timedelta
) -> str:
    return create_token(user_id, username, user_type, expires_delta, 'refresh')


def create_token(
    user_id: str,
    username: str,
    user_type: str,
    expires_delta: timedelta,
    token_type: str,
) -> str:
    expire = datetime.now(tz=UTC) + expires_delta
    to_encode = {
        'sub': username,
        'user_id': user_id,
        'user_type': user_type,
        'exp': expire,
        'token_type': token_type,
    }
    encoded_jwt = jwt.encode(to_encode, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)
) -> User:
    decoded_token = validate_token(token)
    user = db.get(User, decoded_token['user_id'])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return cast(User, user)


def validate_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from None
