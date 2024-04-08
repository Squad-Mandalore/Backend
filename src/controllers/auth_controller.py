from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import User
from src.schemas import auth_schema, user_schema
from src.services import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    #responses={404: {"route": "Not found"}}
)

@router.post("/login", response_model=auth_schema.Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.get_tokens(form_data, db)

@router.post("/refresh", response_model=auth_schema.Token, status_code=status.HTTP_200_OK)
async def refresh_access_token(x_refresh_token: str = Header(), db: Session = Depends(get_db)):
    return auth_service.get_refreshed_tokens(x_refresh_token, db)

@router.get("/whoami", response_model=user_schema.UserResponseSchema, status_code=status.HTTP_200_OK)
async def who_am_i(user: User = Depends(auth_service.get_current_user)):
    return user
