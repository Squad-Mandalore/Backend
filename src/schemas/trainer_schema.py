from datetime import date
from typing import Optional
from src.schemas.user_schema import UserResponseSchema


class TrainerResponseSchema(UserResponseSchema):
    id: str
