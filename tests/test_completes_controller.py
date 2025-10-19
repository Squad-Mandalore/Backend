from datetime import date

from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.models import Athlete, Exercise, Trainer
from src.models.values import parse_values
from tests.define_test_variables import TestVariables, client_fixture, session_fixture

client = client_fixture
session = session_fixture


def test_create_completes(session: Session, client: TestClient) -> None:
    parse_values(session)
    exercise: Exercise = session.scalars(
        select(Exercise).where(Exercise.title == '800 m Lauf')
    ).one()
    session.add(exercise)

    trainer: Trainer = Trainer(
        username='trainer',
        email='trainer',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.flush()

    athlete: Athlete = Athlete(
        username='athlete_completes',
        email='athlete',
        unhashed_password='athlete',
        firstname='athlete',
        lastname='athlete',
        birthday=date.today(),
        trainer_id=trainer.id,
    )
    session.add(athlete)
    session.commit()

    body = {
        'exercise_id': exercise.id,
        'athlete_id': athlete.id,
        'result': '00:05:00:000',
    }
    response: Response = client.post(
        '/completes', json=body, headers=TestVariables.headers
    )
    TestVariables.test_completes = response.json()
    assert response.status_code == 201, f'{str(response.status_code)} {response.json()}'
    assert response.json()['result'] == '00:05:00:000'


def test_get_completes_by_id(client: TestClient):
    response = client.get('/completes/', headers=TestVariables.headers)
    assert response.status_code == 200, f'{str(response.status_code)} {response.json()}'
    assert response.json()[0]['result'] == '00:05:00:000'

    response = client.get(
        f'/completes/?exercise_id={TestVariables.test_completes["exercise"]["id"]}',
        headers=TestVariables.headers,
    )
    assert response.status_code == 200
    assert response.json()[0]['result'] == '00:05:00:000'

    response = client.get(
        f'/completes/?athlete_id={TestVariables.test_completes["athlete_id"]}',
        headers=TestVariables.headers,
    )
    assert response.status_code == 200
    assert response.json()[0]['result'] == '00:05:00:000'

    response = client.get(
        f'/completes/?tracked_at={TestVariables.test_completes["tracked_at"]}',
        headers=TestVariables.headers,
    )
    assert response.status_code == 200
    assert response.json()[0]['result'] == '00:05:00:000'

    response = client.get(
        f'/completes/?exercise_id={TestVariables.test_completes["exercise"]["id"]}&athlete_id={TestVariables.test_completes["athlete_id"]}',
        headers=TestVariables.headers,
    )
    assert response.status_code == 200
    assert response.json()[0]['result'] == '00:05:00:000'

    response = client.get(
        f'/completes/?exercise_id={TestVariables.test_completes["exercise"]["id"]}&tracked_at={TestVariables.test_completes["tracked_at"]}',
        headers=TestVariables.headers,
    )
    assert response.status_code == 200
    assert response.json()[0]['result'] == '00:05:00:000'

    response = client.get(
        f'/completes/?athlete_id={TestVariables.test_completes["athlete_id"]}&tracked_at={TestVariables.test_completes["tracked_at"]}',
        headers=TestVariables.headers,
    )
    assert response.status_code == 200
    assert response.json()[0]['result'] == '00:05:00:000'

    response = client.get(
        f'/completes/?exercise_id={TestVariables.test_completes["exercise"]["id"]}&athlete_id={TestVariables.test_completes["athlete_id"]}&tracked_at={TestVariables.test_completes["tracked_at"]}',
        headers=TestVariables.headers,
    )
    assert response.status_code == 200
    assert response.json()[0]['result'] == '00:05:00:000'


def test_patch_completes(client: TestClient) -> None:
    body = {
        'result': '0000000000',
    }
    response: Response = client.patch(
        f'/completes/?exercise_id={TestVariables.test_completes["exercise"]["id"]}&athlete_id={TestVariables.test_completes["athlete_id"]}&tracked_at={TestVariables.test_completes["tracked_at"]}',
        headers=TestVariables.headers,
        json=body,
    )
    assert response.status_code == 202, f'{str(response.status_code)} {response.json()}'
    assert response.json()['result'] == '0000000000'


def test_delete_completes(client: TestClient) -> None:
    response = client.delete(
        f'/completes/?exercise_id={TestVariables.test_completes["exercise"]["id"]}&athlete_id={TestVariables.test_completes["athlete_id"]}&tracked_at={TestVariables.test_completes["tracked_at"]}',
        headers=TestVariables.headers,
    )
    assert response.status_code == 200, f'{str(response.status_code)} {response.json()}'
