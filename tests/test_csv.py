# from tests.define_test_variables import client

from datetime import date
import pytest
from src.models.models import Athlete, Base, Gender, Trainer
from src.services.csv_service import create_csv


@pytest.fixture
def session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Replace the connection string with your actual database connection details.
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    #engine = create_engine("sqlite:///db/test_test.db", echo=True, connect_args={"check_same_thread": False})

    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

def create_athletes(session):
    trainer = Trainer(username="trainer_athlete", email="trainer", hashed_password="trainer", firstname="trainer", lastname="trainer", salt="trainer", uses_otp=False, birthday=None)
    athlete = Athlete(username="athlete", email="athlete", hashed_password="athlete", firstname="athlete", lastname="athlete", salt="athlete", birthday=date.today(), gender=Gender.DIVERSE, has_disease=False, trainer=trainer)
    session.add(trainer)
    session.add(athlete)
    session.add(athlete)
    session.commit()

def test_athlete_csv(session):
    create_athletes(session)
    create_csv(session, Athlete, 'test_athletes.csv')
