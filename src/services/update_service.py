from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime

from src.models.models import Base, User
from src.services import password_service

def update_properties(obj: Base, schema: BaseModel):
    update_fields = schema.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(obj, field, value)

def update_password(user: User, unhashed_password: str) -> None:
    check: HTTPException | None = password_service.validate_password(unhashed_password)
    if check:
        raise check

    hashed_password, _ = password_service.hash_and_spice_password(unhashed_password, user.salt)
    setattr(user, "hashed_password", hashed_password)
    setattr(user, "last_password_change", datetime.now())
