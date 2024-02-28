from typing import Optional

from fastapi import HTTPException


def validate_password(password: str) -> Optional[HTTPException]:
    if len(password) < 12:
        return HTTPException(status_code=400, detail="Password must be at least 12 characters long")

    return None
