from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base_model import Base

# mashallah in memory engine bro
engine = create_engine('sqlite:///db/test.db', connect_args={"check_same_thread": False})

# with sqlalchemy you are able to store python objects in a database,
# therefore you first need to create some python classes

# Set up the session
SessionLocal = sessionmaker(bind=engine)

# create db shiat
def init_db() -> None:
    Base.metadata.create_all(bind=engine)
