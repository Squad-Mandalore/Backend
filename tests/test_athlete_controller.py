from datetime import date
from uuid import UUID

import pytest

from src.models.models import Athlete, Gender, Base
from tests.define_test_variables import client, TestVariables

@pytest.fixture
def session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Replace the connection string with your actual database connection details.
    engine = create_engine("sqlite:///:memory:", echo=True, connect_args={"check_same_thread": False})
    #engine = create_engine("sqlite:///db/test_test.db", echo=True, connect_args={"check_same_thread": False})

    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

def add_test_athlete(session) -> Athlete:
    athlete = Athlete("ole361", "ole@mail", "12345",
                      "oleg", "rundmann", "salzig", date.today(),
                      UUID("16d094b1-e9cf-4cf4-b3ea-6a832582adf2"), True,
                      Gender.MALE)
    session.add(athlete)
    athleteDb = session.query(Athlete).first()
    return athleteDb

def test_get_all_athletes(session) -> None:
    athleteDb = add_test_athlete(session)
    response = client.get(TestVariables.BASEURL + "/athletes/all", headers=TestVariables.HEADERS)
    assert response.status_code == 202

def test_get_athlete_by_id(session) -> None:
    athleteDb = add_test_athlete(session)
    response = client.get(TestVariables.BASEURL + f"/athletes/{athleteDb.id}", headers=TestVariables.HEADERS)
    assert response.status_code == 202

def test_delete_athlete(session) -> None:
    athleteDb = add_test_athlete(session)
    response = client.delete(TestVariables.BASEURL + f"/athletes/{athleteDb.id}", headers=TestVariables.HEADERS)
    assert response.status_code == 204

def test_post_athlete() -> None:
    body = {
    "username": "benole",
    "email": "ole@mail",
    "password": "nicht-gehashed",
    "firstname": "ole",
    "lastname": "grundmann",
    "birthday": "2024-02-18",
    "trainer_id": "16d094b1-e9cf-4cf4-b3ea-6a832582adf2",
    "has_disease": true,
    "gender": "m"
    }
    response = client.post(TestVariables.BASEURL + "/athletes", json=body,  headers=TestVariables)
    assert response.status_code == 201

def test_put_athlete(session) -> None:
    athleteDb = add_test_athlete(session)
    body = {
        "firstname": "markus",
        "lastname": "quarkus"
    }
    response = client.put(TestVariables.BASEURL + f"/athletes/{athleteDb.id}",json=body, headers=TestVariables.HEADERS)
    athlete = session.query(Athlete).first()
    assert athlete.firstname == "markus"
    assert athlete.lastname == "quarkus"