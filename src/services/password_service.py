import hashlib
from ..database.database_utils import add
from ..models.user_model import User

KEYCHAIN_NUMBER = 42
PEPPER = "for the rizzler"


def password_service(password):
    salted_password, salt = salt_password(password)
    peppered_password = pepper_password(salted_password)
    hashed_password = hash_password(peppered_password)
    user = User(hashed_password, salt)
    add(user)        # TODO later only return hashed password and salt for atomar desgin
    return user


def salt_password(password, salt=None):
    if salt is None:
        generated_salt = generate_salt()
        salted_password = apply_salt(password, generated_salt)
        return salted_password, generated_salt
    else:
        salted_password = apply_salt(password, salt)
        return salted_password, salt


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


def hash_password(password, keychain_number=KEYCHAIN_NUMBER):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    for _ in range(keychain_number - 1):
        hashed_password = hashlib.sha256(hashed_password.encode()).hexdigest()

    return hashed_password