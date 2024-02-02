from fastapi import HTTPException


def validate_password(password: str) -> None:
    if len(password) < 12:
        raise HTTPException(status_code=400, detail="Password must be at least 12 characters long")
