from src.database.database_setup import session
from src.models.user_model import User
from src.services.password_service import salt_password, pepper_password, hash_password

salt = None
def check_password(id, password):

    password_list = session.query(User).filter(User.id == id).filter(User.password).first()
    password_db = ''.join(password_list)
    salt_list = session.query(User).filter(User.id == id).filter(User.salt).first()
    salt_db = ''.join(salt_list)


    salted_password = salt_password(password, salt)
    peppered_password = pepper_password(salted_password)
    hashed_password = hash_password(peppered_password)

    if hashed_password == password:
        # Password is correct
        return True
    else:
        # Password is incorrect or user not found
        return False
