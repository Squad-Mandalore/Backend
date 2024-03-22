from src.services.csv_service import create_csv, entity_config, parse_csv
from tests.define_test_variables import client_fixture, session_fixture, TestVariables
from datetime import date, datetime
from src.models.models import Athlete, Base, Category, Completes, Exercise, Gender, Trainer

def create_athletes(session):
    trainer = Trainer(username="trainer_athlete_completes", email="trainer", unhashed_password="trainer", firstname="trainer", lastname="trainer")
    session.add(trainer)
    session.flush()
    athlete = Athlete(username="athlete_completes", email="athlete", unhashed_password="athlete", firstname="athlete", lastname="athlete",  birthday=date.today(), gender=Gender.DIVERSE, trainer_id=trainer.id)
    session.add(athlete)
    session.flush()
    category = Category(title="category_exercise_completes")
    session.add(category)
    session.flush()
    exercise = Exercise(title="exercise_completes", category_id=category.id, from_age=10, to_age=20)
    session.add(exercise)
    session.flush()
    completes = Completes(athlete_id=athlete.id, exercise_id=exercise.id, tracked_at=datetime.now(), tracked_by=trainer.id, result="result", points=1)
    session.add(completes)
    session.commit()

def test_csv(session, client):
    create_athletes(session)
    response = client.get(TestVariables.BASEURL + "/csv/trainer.csv")
    assert response.status_code == 200, f"{response.text} {response.status_code}"
    response = client.get(TestVariables.BASEURL + "/csv/athlete.csv")
    assert response.status_code == 200, f"{response.text} {response.status_code}"
    response = client.get(TestVariables.BASEURL + "/csv/completes.csv")
    assert response.status_code == 200, f"{response.text} {response.status_code}"

    response = client.post(TestVariables.BASEURL + "/csv/parse", files={"file": ("trainer.csv", open("trainer.csv", "rb"))}, headers=TestVariables.headers)
    assert response.status_code == 400, f"{response.text} {response.status_code}"
    response = client.post(TestVariables.BASEURL + "/csv/parse", files={"file": ("athlete.csv", open("athlete.csv", "rb"))}, headers=TestVariables.headers)
    assert response.status_code == 201, f"{response.text} {response.status_code}"
    response = client.post(TestVariables.BASEURL + "/csv/parse", files={"file": ("completes.csv", open("completes.csv", "rb"))}, headers=TestVariables.headers)
    assert response.status_code == 201, f"{response.text} {response.status_code}"
