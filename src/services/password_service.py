import hashlib
import os
import random
from collections.abc import Callable
from random import choice
from string import ascii_letters

from fastapi import HTTPException

KEYCHAIN_NUMBER = int(os.getenv('KEYCHAIN_NUMBER', 42))
PEPPER = os.getenv(
    'PEPPER', "I'm a pepper, you're a pepper, wouldn't you like to be a pepper too?"
)


# this function is the entrypoint for hashing and spicing a password
def hash_and_spice_password(password: str, salt: str = '') -> tuple[str, str]:
    salted_password, salt = salt_password(password, salt)
    peppered_password = pepper_password(salted_password)
    hashed_password = hash_password(peppered_password)

    return hashed_password, salt


def salt_password(password: str, salt: str) -> tuple[str, str]:
    generated_salt = salt

    if generated_salt == '':
        generated_salt = generate_salt()

    salted_password = apply_salt(password, generated_salt)
    return salted_password, generated_salt


def generate_salt(salt_length: int = 0) -> str:
    if salt_length == 0:
        salt_length = random.randint(1, 255)

    salt = ''.join(choice(ascii_letters) for _ in range(salt_length))
    return salt


def apply_salt_func(password: str, salt: str) -> str:
    return password + salt


def apply_salt(
    password: str,
    salt: str,
    apply_salt_func: Callable[[str, str], str] = apply_salt_func,
) -> str:
    salted_password = apply_salt_func(password, salt)
    return salted_password


def pepper_password_func(password: str) -> str:
    return password + PEPPER


def pepper_password(
    password: str, apply_pepper_func: Callable[[str], str] = pepper_password_func
) -> str:
    peppered_password = apply_pepper_func(password)
    return peppered_password


def hash_password(password: str, keychain_number: int = KEYCHAIN_NUMBER) -> str:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    for _ in range(keychain_number - 1):
        hashed_password = hashlib.sha256(hashed_password.encode()).hexdigest()

    return hashed_password


def verify_password(user, password: str) -> bool:
    # check the password
    hashed_password, _ = hash_and_spice_password(password, user.salt)
    return hashed_password == user.hashed_password


def validate_password(password: str) -> HTTPException | None:
    if len(password) < 12:
        return HTTPException(
            status_code=400, detail='Password must be at least 12 characters long'
        )

    return None
