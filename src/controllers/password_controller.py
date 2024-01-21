from fastapi import APIRouter

from ..schemas.password_schema import PasswordSchema
from ..services.password_service import password_service

router = APIRouter()

# Your routes could be listed here
