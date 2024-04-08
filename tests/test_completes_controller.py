from datetime import date
from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.models import Athlete, Exercise, Trainer
from src.models.values import parse_values
from tests.define_test_variables import TestVariables, client_fixture, session_fixture
from src.logger.logger import logger

client = client_fixture
session = session_fixture

def test_create_completes(session: Session, client: TestClient) -> None:
    parse_values(session)
    response = client.get('/exercises', headers=TestVariables.headers)
    TestVariables.test_exercise = response.json()[0]

    trainer: Trainer = Trainer(username='trainer', email='trainer', unhashed_password='trainer', firstname='trainer', lastname='trainer')
    session.add(trainer)
    session.flush()

    athlete: Athlete = Athlete(username='athlete_completes', email='athlete', unhashed_password='athlete', firstname='athlete', lastname='athlete',  birthday=date.today(), trainer_id=trainer.id)
    session.add(athlete)
    session.commit()

    body = {
        'exercise_id': TestVariables.test_exercise['id'],
        'athlete_id': athlete.id,
        'result': 'I like Coco',
        'points': 3
    }
    response: Response = client.post('/completes', json=body, headers=TestVariables.headers)
    TestVariables.test_completes = response.json()
    assert response.status_code == 201, f'{str(response.status_code)} {response.json()}'
    assert response.json()['result'] == 'I like Coco'
    assert response.json()['points'] == 3

def test_get_completes_by_id(client: TestClient):
    response = client.get(f"/completes/", headers=TestVariables.headers)
    assert response.status_code == 200, f'{str(response.status_code)} {response.json()}'
    assert response.json()[0]['result'] == 'I like Coco'

    response = client.get(f"/completes/?exercise_id={TestVariables.test_completes['exercise']['id']}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()[0]['result'] == 'I like Coco'

    response = client.get(f"/completes/?athlete_id={TestVariables.test_completes['athlete_id']}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()[0]['result'] == 'I like Coco'

    response = client.get(f"/completes/?tracked_at={TestVariables.test_completes['tracked_at']}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()[0]['result'] == 'I like Coco'

    response = client.get(f"/completes/?exercise_id={TestVariables.test_completes['exercise']['id']}&athlete_id={TestVariables.test_completes['athlete_id']}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()[0]['result'] == 'I like Coco'

    response = client.get(f"/completes/?exercise_id={TestVariables.test_completes['exercise']['id']}&tracked_at={TestVariables.test_completes['tracked_at']}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()[0]['result'] == 'I like Coco'

    response = client.get(f"/completes/?athlete_id={TestVariables.test_completes['athlete_id']}&tracked_at={TestVariables.test_completes['tracked_at']}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()[0]['result'] == 'I like Coco'

    response = client.get(f"/completes/?exercise_id={TestVariables.test_completes['exercise']['id']}&athlete_id={TestVariables.test_completes['athlete_id']}&tracked_at={TestVariables.test_completes['tracked_at']}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()[0]['result'] == 'I like Coco'

def test_patch_completes(client: TestClient) -> None:
    body = {
        'result': '0000000000',
    }
    response: Response = client.patch(f"/completes/?exercise_id={TestVariables.test_completes['exercise']['id']}&athlete_id={TestVariables.test_completes['athlete_id']}&tracked_at={TestVariables.test_completes['tracked_at']}", headers=TestVariables.headers, json=body)
    assert response.status_code == 202, f'{str(response.status_code)} {response.json()}'
    assert response.json()['result'] == '0000000000'

def test_delete_completes(client: TestClient) -> None:
    response = client.delete(f"/completes/?exercise_id={TestVariables.test_completes['exercise']['id']}&athlete_id={TestVariables.test_completes['athlete_id']}&tracked_at={TestVariables.test_completes['tracked_at']}", headers=TestVariables.headers)
    assert response.status_code == 200, f'{str(response.status_code)} {response.json()}'
