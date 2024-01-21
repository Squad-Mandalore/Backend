from fastapi import APIRouter

from ..schemas.password_schema import PasswordSchema
from ..services.password_service import password_service

router = APIRouter()


@router.post("/password")
async def post_password(password_schema: PasswordSchema):
    password = password_schema.password
    user = password_service(password)
    return user
