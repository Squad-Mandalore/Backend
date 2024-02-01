def validate_password(password: str) -> bool:
    if len(password) >= 12:
        return True
    return False
