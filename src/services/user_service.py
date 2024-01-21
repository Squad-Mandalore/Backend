from src.database.database_setup import session
from src.models.user_model import User
from src.services.password_service import salt_password, pepper_password, hash_password

salt = None
def check_password(id, password):

    # password_db = session.query(User).filter(User.id == id).filter(User.password).first()
    # password_db = ''.join(password_list)
    user = session.query(User).filter(User.id == id).first()
    if user:
        print(f"User found: {user}")
    else:
        print(f"No user found with this id: {id}")
    # salt_db = ''.join(salt_list)

    salted_password, _ = salt_password(user.password, user.salt)
    peppered_password = pepper_password(salted_password)
    hashed_password = hash_password(peppered_password)

    if hashed_password == password:
        # Password is correct
        return "True"
    else:
        # Password is incorrect or user not found
        return "False"
