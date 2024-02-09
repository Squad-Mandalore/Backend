import hashlib
from src.services.password_service import KEYCHAIN_NUMBER, PEPPER, generate_salt, hash_and_spice_password, hash_password, pepper_password, salt_password


# Test `generate_salt` function
def test_generate_salt():
    salt = generate_salt(10)
    assert len(salt) == 10, "Salt length should be 10"
    assert salt.isalpha(), "Salt should only contain letters"

# Test `salt_password` function
def test_salt_password():
    password = "spam and eggs"
    salt = "salt"
    salted_password, used_salt = salt_password(password, salt)
    assert salted_password == password + salt, "Salted password does not match expected value"
    assert used_salt == salt, "Used salt does not match provided salt"

# Test `pepper_password` function
def test_pepper_password():
    password = "spam and eggs"
    peppered_password = pepper_password(password)
    assert peppered_password == password + PEPPER, "Peppered password does not match expected value"

# Test `hash_password` function with a known result to ensure consistent hashing
def test_hash_password():
    password = "spam and eggs" + "salt" + PEPPER
    hashed_password = hash_password(password)
    # Expected result obtained by manually hashing the concatenated string
    expected_hash = hashlib.sha256(password.encode()).hexdigest()
    for _ in range(KEYCHAIN_NUMBER - 1):
        expected_hash = hashlib.sha256(expected_hash.encode()).hexdigest()
    assert hashed_password == expected_hash, "Hashed password does not match expected hash"

# Test `hash_and_spice_password` function to ensure it integrates well
def test_hash_and_spice_password():
    password = "spam and eggs"
    hashed_password, salt = hash_and_spice_password(password)
    # Validate returned values are in expected format without knowing the exact outcome due to randomness in salt
    assert isinstance(hashed_password, str) and len(hashed_password) > 0, "Hashed password should be a non-empty string"
    assert isinstance(salt, str) and len(salt) > 0, "Salt should be a non-empty string"

