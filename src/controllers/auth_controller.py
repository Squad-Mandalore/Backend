from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.schemas.auth_schema import Token
from src.services import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"route": "Not found"}}
)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await auth_service.get_token(form_data, db)

#route for refreshing the access token
@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await auth_service.get_refresh_token(refresh_token, db)
