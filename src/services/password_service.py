import hashlib
from random import choice
from string import ascii_letters
import random

# TODO: Those 2 should not be visible like this, they should be set at environment level (we are a public repo)
# This can be done via GitHub secrets and our CI/CD pipeline
KEYCHAIN_NUMBER = 42
PEPPER = "I would rather be programming Go right now"


def hash_and_spice_password(password, salt=None):
    salted_password, salt = salt_password(password, salt)
    peppered_password = pepper_password(salted_password)
    hashed_password = hash_password(peppered_password)
    return hashed_password, salt


def salt_password(password, salt):
    generated_salt = salt

    if generated_salt is None:
        generated_salt = generate_salt()

    salted_password = apply_salt(password, generated_salt)
    return salted_password, generated_salt


def generate_salt(salt_length=None):
    if salt_length is None:
        salt_length = random.randint(1, 255)
    salt = "".join(choice(ascii_letters) for _ in range(salt_length))
    return salt

def apply_salt_func(password, salt):
    return password + salt

def apply_salt(password, salt, apply_salt_func=apply_salt_func):
    salted_password = apply_salt_func(password, salt)
    return salted_password

def pepper_password_func(password):
    return password + PEPPER

def pepper_password(password, apply_pepper_func=pepper_password_func):
    peppered_password = apply_pepper_func(password)
    return peppered_password

def hash_password(password, keychain_number=KEYCHAIN_NUMBER):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    for _ in range(keychain_number - 1):
        hashed_password = hashlib.sha256(hashed_password.encode()).hexdigest()

    return hashed_password
