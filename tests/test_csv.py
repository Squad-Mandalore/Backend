# from tests.define_test_variables import client

from datetime import date, datetime
import pytest
from src.models.models import Athlete, Base, Category, Completes, Exercise, Gender, Trainer
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
    trainer = Trainer(username="trainer_athlete_completes", email="trainer", unhashed_password="trainer", firstname="trainer", lastname="trainer", uses_otp=False, birthday=None)
    session.add(trainer)
    session.commit()
    trainerDb = session.query(Trainer).filter(Athlete.username == "trainer_athlete_completes").first()
    athlete = Athlete(username="athlete_completes", email="athlete", unhashed_password="athlete", firstname="athlete", lastname="athlete",  birthday=date.today(), gender=Gender.DIVERSE, has_disease=False, trainer_id=trainerDb.id)
    session.add(athlete)
    session.commit()
    athleteDb = session.query(Athlete).filter(Athlete.username == "athlete_completes").first()
    category = Category(title="category_exercise_completes")
    session.add(category)
    session.commit()
    categoryDb = session.query(Category).filter(Category.title == "category_exercise_completes").first()
    exercise = Exercise(title="exercise_completes", category_id=categoryDb.id, from_age=10, to_age=20)
    session.add(exercise)
    session.commit()
    exerciseDb = session.query(Exercise).filter(Exercise.title == "exercise_completes").first()
    completes = Completes(athlete_id=athleteDb.id, exercise_id=exerciseDb.id, tracked_at=datetime.now(), completed_at=datetime.now(), result="result", points=1)
    session.add(completes)
    session.commit()

def test_csv(session):
    create_athletes(session)
    create_csv(session)
    # parse_csv(session)
