from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel

from src.models.models import Base
from src.models.models import User
from src.services import password_service


def update_properties(obj: Base, schema: BaseModel):
    update_fields = schema.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(obj, field, value)


def update_password(user: User, unhashed_password: str) -> None:
    check: HTTPException | None = password_service.validate_password(unhashed_password)
    if check:
        raise check

    hashed_password, _ = password_service.hash_and_spice_password(
        unhashed_password, user.salt
    )
    user.hashed_password = hashed_password
    user.last_password_change = datetime.now()
