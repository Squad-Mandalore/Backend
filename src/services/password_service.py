import hashlib
from ..database.database_utils import add
from ..models.password_model import Password

KEYCHAIN_NUMBER = 42
PEPPER = "for the rizzler"


def password_service(password):
    salted_password = salt_password(password)
    peppered_password = pepper_password(salted_password)
    hashed_password = hash_password(peppered_password)
    add(hashed_password)


def salt_password(password):
    salt = generate_salt()
    password = apply_salt(password, salt)
    return Password(password, salt)


def generate_salt():
    # some generation stuff
    return "sticking out your gyat"


def apply_salt(password, salt, apply_salt_func=None):
    if apply_salt_func is None:
        salted_password = password + salt
    else:
        salted_password = apply_salt_func(password, salt)

    return salted_password


def pepper_password(password, apply_pepper_func=None):
    if apply_pepper_func is None:
        peppered_password = password + PEPPER
    else:
        peppered_password = apply_pepper_func(password)

    return peppered_password


def hash_password(password, keychain_number):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    for _ in range(keychain_number - 1):
        hashed_password = hashlib.sha256(hashed_password.encode()).hexdigest()

    return hashed_password
