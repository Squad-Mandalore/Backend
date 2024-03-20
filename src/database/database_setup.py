import os
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import Session
from src.logger.logger import logger
from src.models.models import Administrator, Base
from src.models.values import parse_values

db_path: str = '/db/test.db'
engine = create_engine(f'sqlite://{db_path}', connect_args={"check_same_thread": False})

# with sqlalchemy you are able to store python objects in a database,
# therefore you first need to create some python classes

# create db shiat
def init_db() -> None:
    if not os.path.exists(f'.{db_path}'):
        logger.info("Creating database")
        Base.metadata.create_all(bind=engine)
        parse_values(Session(engine))

@event.listens_for(Administrator.__table__, "after_create")
def insert_initial_data(target, connection, **kw) -> None:
    with Session(connection.engine) as session:
        admin = Administrator(username="init", unhashed_password="admin", email="admin", firstname="admin", lastname="admin", uses_otp=False)
        session.add(admin)
        session.commit()
    logger.info("Inserted initial data")
