from sqlalchemy import Column, String
from ..database.database_setup import Base
from ..database.database_utils import get_uuid


class User(Base):
    __tablename__ = 'user'
    id = Column("id", String, primary_key=True)
    # TODO combine id and username as primery key
    username = Column("username", String)
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

    def __repr__(self):
        return f"{self.password}, {self.salt}"
