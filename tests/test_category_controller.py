from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.models import Athlete, Trainer
from src.models.values import parse_values
from tests.define_test_variables import TestVariables, client_fixture, session_fixture
from src.logger.logger import logger

client = client_fixture
session = session_fixture


def test_get_category_by_id(session: Session, client: TestClient):
    parse_values(session)
    response = client.get('/exercises', headers=TestVariables.headers)
    TestVariables.test_exercise = response.json()[0]

    trainer: Trainer = Trainer(username='trainer', email='trainer', unhashed_password='trainer', firstname='trainer', lastname='trainer')
    session.add(trainer)
    session.flush()

    athlete: Athlete = Athlete(username='athlete_completes', email='athlete', unhashed_password='athlete', firstname='athlete', lastname='athlete',  birthday=date.today(), trainer_id=trainer.id)
    session.add(athlete)
    session.commit()

    response = client.get(f"/categories", headers=TestVariables.headers)
    assert response.status_code == 200
    assert len(response.json()) == 4
    TestVariables.test_category = response.json()[0]

    response = client.get(f"/categories?category_id={TestVariables.test_category['id']}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get(f"/categories?athlete_id={athlete.id}", headers=TestVariables.headers)
    assert response.status_code == 200, f"{str(response.status_code)} {response.json()}"
