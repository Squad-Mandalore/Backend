import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.models import Base
from src.models.values import parse_values
from src.logger.logger import logger

db_path: str = '/db/test.db'
engine = create_engine(f'sqlite://{db_path}', connect_args={"check_same_thread": False})

# with sqlalchemy you are able to store python objects in a database,
# therefore you first need to create some python classes

# Set up the session
SessionLocal = sessionmaker(bind=engine)

# create db shiat
def init_db() -> None:
    if not os.path.exists('.' + db_path):
        logger.info("Creating database")
        Base.metadata.create_all(bind=engine)
        parse_values(SessionLocal())
