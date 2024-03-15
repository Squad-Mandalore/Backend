from src.services.csv_service import create_csv, entity_config
from tests.define_test_variables import client, TestVariables
from datetime import date, datetime
import pytest
from src.models.models import Athlete, Base, Category, Completes, Exercise, Gender, Trainer

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
    athlete = Athlete(username="athlete_completes", email="athlete", unhashed_password="athlete", firstname="athlete", lastname="athlete",  birthday=date.today(), gender=Gender.DIVERSE, has_disease=False, trainer_id=trainer.id)
    session.add(athlete)
    session.commit()
    category = Category(title="category_exercise_completes")
    session.add(category)
    session.commit()
    exercise = Exercise(title="exercise_completes", category_id=category.id, from_age=10, to_age=20)
    session.add(exercise)
    session.commit()
    completes = Completes(athlete_id=athlete.id, exercise_id=exercise.id, tracked_at=datetime.now(), completed_at=datetime.now(), result="result", points=1)
    session.add(completes)
    session.commit()

def test_csv(session):
    create_athletes(session)
    create_csv(session)
    response = client.get(TestVariables.BASEURL + "/csv/trainer.csv")
    assert response.status_code == 200, response.text
    response = client.get(TestVariables.BASEURL + "/csv/athlete.csv")
    assert response.status_code == 200, response.text
    response = client.get(TestVariables.BASEURL + "/csv/completes.csv")
    assert response.status_code == 200, response.text
    # parse_csv(session)
