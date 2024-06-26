from fastapi import HTTPException
from src.services.password_service import validate_password


def test_validate_password():
    # Test `validate_password` function
    # first case is a valid password
    assert None == validate_password("spam and eggs")
    # second case is an invalid password
    assert isinstance(validate_password("spam"), HTTPException)
    # third case is a valid password and checks for special characters
    assert None == validate_password("späm🥫🥫🥫 and ëggs🥚🥚🥚")
