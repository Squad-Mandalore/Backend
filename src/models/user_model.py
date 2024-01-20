from sqlalchemy import Column, String, Integer
from ..database.database_setup import Base
from ..database.database_utils import get_uuid


class User(Base):
    __tablename__ = 'user'
    id = Column("id", String, primary_key=True)
    username = Column("username", String)       #TODO combine id and username as primery key
    password = Column("password", String)
    salt = Column("salt", String)
    lastname = Column("lastname", String)
    forename = Column("forename", String)
    created_at = Column("created_at", String)
    last_edited_at = Column("last_edited_at", String)
    last_password_change = Column("last_password_change", String)
    email = Column("email", String)

    def __init__(self, password, salt):
        self.id = get_uuid()
        self.password = password
        self.salt = salt


