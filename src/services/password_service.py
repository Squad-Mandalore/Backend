import hashlib
from random import choice
from string import ascii_letters
import random

KEYCHAIN_NUMBER = 42
PEPPER = "I would rather be programming Go right now"


def encrypt_password(password):
    salted_password, salt = salt_password(password)
    peppered_password = pepper_password(salted_password)
    hashed_password = hash_password(peppered_password)
    return hashed_password, salt


def salt_password(password, salt=None):
    if salt is None:
        generated_salt = generate_salt()
        salted_password = apply_salt(password, generated_salt)
        return salted_password, generated_salt
    else:
        salted_password = apply_salt(password, salt)
        return salted_password, salt


def generate_salt(l=None):
    if l is None:
        l = random.randint(1, 1000)
    salt = "".join(choice(ascii_letters) for _ in range(l))
    return salt


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
