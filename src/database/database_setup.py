from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# mashallah in memory engine bro
engine = create_engine('sqlite:///:memory:')

# with sqlalchemy you are able to store python objects in a database,
# therefore you first need to create some python classes

# Base class to inherit from
Base = declarative_base()

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()


# create db shiat
def init_db():
    Base.metadata.create_all(bind=engine)
