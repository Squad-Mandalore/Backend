from sqlalchemy import Column, String, Integer
from ..database.database_setup import Base


class Password(Base):
    __tablename__ = 'passwords'
    id = Column("id", Integer, primary_key=True)
    password = Column("password", String)
    salt = Column("salt", String)
