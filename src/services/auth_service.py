from datetime import datetime, timedelta, timezone
from os import getenv
from typing import Literal, Optional, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session

from src.database.database_utils import get_by_id, get_db
from src.models.models import User
from src.schemas.auth_schema import Token
from src.services.password_service import hash_and_spice_password


ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

def authenticate_user(username: str, password: str, db: Session) -> User | Literal[False]:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(user, password):
        return False
    return user

async def get_token(form_data, db: Session) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return await get_user_tokens(user)

async def get_refresh_token(refresh_token: str, db: Session) -> Token:
    return await get_user_tokens(get_current_user(refresh_token,db), refresh_token)

async def get_user_tokens(user: User, refresh_token: Optional[str] = None):
    access_token = create_access_token(user.id, user.username, user.type, timedelta(minutes=1))
    if not refresh_token:
        refresh_token = create_refresh_token(user.id, user.username, user.type, timedelta(days=30))

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

def create_access_token(user_id: str, username: str, user_type: str, expires_delta: pitimedelta) -> str:
    expire = datetime.now(tz=timezone.utc) + expires_delta
    token_type = "access"
    to_encode = {"sub": username, "user_id": user_id, "user_type": user_type, "exp": expire, "token_type": token_type}
    encoded_jwt = jwt.encode(to_encode, getenv('JWT_KEY', 'test'), algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: str, username: str, user_type: str, expires_delta: timedelta) -> str:
    expire = datetime.now(tz=timezone.utc) + expires_delta
    token_type = "refresh"
    to_encode = {"sub": username, "user_id": user_id, "user_type": user_type, "exp": expire, "token_type": token_type}
    encoded_jwt = jwt.encode(to_encode, getenv('JWT_KEY', 'test'), algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_bearer), db: Session  = Depends(get_db)) -> User | None:
    try:
        payload = jwt.decode(token, getenv('JWT_KEY', 'test'), algorithms=[ALGORITHM])
        user = get_by_id(User, payload["user_id"], db)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return cast(User, user)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

def verify_password(user: User, password: str) -> bool:
    # check the password
    hashed_password, _ = hash_and_spice_password(password, user.salt)
    return hashed_password == user.hashed_password
