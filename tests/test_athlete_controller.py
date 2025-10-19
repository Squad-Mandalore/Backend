from datetime import datetime

from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

# client_fixture, session_fixture are fixtures that are used to create a test client and a session for the test cases !!DO NOT REMOVE!!
from src.models.models import Trainer
from src.services import athlete_service, password_service
from tests.define_test_variables import TestVariables


def test_post_athlete(session: Session, client: TestClient):
    trainer: Trainer = Trainer(
        username='trainer',
        email='trainer',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()

    body = {
        'username': 'username',
        'email': 'ole@mail',
        'unhashed_password': 'nicht-gehashed',
        'firstname': 'ole',
        'lastname': 'grundmann',
        'birthday': '2024-02-18',
        'trainer_id': f'{trainer.id}',
        'gender': 'm',
    }

    response = client.post('/athletes', json=body, headers=TestVariables.headers)
    assert response.status_code == 201, f'{response.status_code} {response.json()}'


def test_get_all_athletes(client: TestClient, session: Session):
    # Ensure there's at least one athlete in the database
    trainer: Trainer = Trainer(
        username='trainer_for_all',
        email='trainer_for_all',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()

    athlete_body = {
        'username': 'test_athlete_for_all',
        'email': 'test@email.com',
        'unhashed_password': 'password',
        'firstname': 'test',
        'lastname': 'athlete',
        'birthday': '2024-02-18',
        'trainer_id': f'{trainer.id}',
        'gender': 'm',
    }

    # Create an athlete first
    create_response = client.post(
        '/athletes', json=athlete_body, headers=TestVariables.headers
    )
    assert create_response.status_code == 201

    # Now test getting all athletes
    response = client.get('/athletes', headers=TestVariables.headers)
    assert response.status_code == 200, f' {str(response.status_code)}'
    assert len(response.json()) > 0
    TestVariables.test_athlete = response.json()[0]


def test_get_athlete_by_id(client: TestClient, session: Session):
    # Create a trainer and athlete for this test
    trainer: Trainer = Trainer(
        username='trainer_for_get_by_id',
        email='trainer_for_get_by_id',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()

    athlete_body = {
        'username': 'test_athlete_for_get_by_id',
        'email': 'test_get_by_id@email.com',
        'unhashed_password': 'password',
        'firstname': 'test',
        'lastname': 'athlete',
        'birthday': '2024-02-18',
        'trainer_id': f'{trainer.id}',
        'gender': 'm',
    }

    # Create an athlete first
    create_response = client.post(
        '/athletes', json=athlete_body, headers=TestVariables.headers
    )
    assert create_response.status_code == 201
    athlete_id = create_response.json()['id']

    # Now test getting athlete by id
    response = client.get(f'/athletes/{athlete_id}', headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()['username'] == 'test_athlete_for_get_by_id'


def test_get_full_athlete_by_id(client: TestClient, session: Session):
    # Create a trainer and athlete for this test
    trainer: Trainer = Trainer(
        username='trainer_for_full',
        email='trainer_for_full',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()

    athlete_body = {
        'username': 'test_athlete_for_full',
        'email': 'test_full@email.com',
        'unhashed_password': 'password',
        'firstname': 'test',
        'lastname': 'athlete',
        'birthday': '2024-02-18',
        'trainer_id': f'{trainer.id}',
        'gender': 'm',
    }

    # Create an athlete first
    create_response = client.post(
        '/athletes', json=athlete_body, headers=TestVariables.headers
    )
    assert create_response.status_code == 201
    athlete_id = create_response.json()['id']

    # Now test getting full athlete by id
    response = client.get(f'/athletes/{athlete_id}/full', headers=TestVariables.headers)
    assert response.status_code == 200


def test_patch_athlete(client: TestClient, session: Session) -> None:
    # Create a trainer and athlete for this test
    trainer: Trainer = Trainer(
        username='trainer_for_patch',
        email='trainer_for_patch',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()

    athlete_body = {
        'username': 'test_athlete_for_patch',
        'email': 'test_patch@email.com',
        'unhashed_password': 'nicht-gehashed',
        'firstname': 'original',
        'lastname': 'name',
        'birthday': '2024-02-18',
        'trainer_id': f'{trainer.id}',
        'gender': 'm',
    }

    # Create an athlete first
    create_response = client.post(
        '/athletes', json=athlete_body, headers=TestVariables.headers
    )
    assert create_response.status_code == 201
    athlete_id = create_response.json()['id']

    # Now test patching the athlete
    body = {'firstname': 'markus', 'lastname': 'quarkus'}
    response: Response = client.patch(
        f'/athletes/{athlete_id}', json=body, headers=TestVariables.headers
    )
    assert password_service.verify_password(
        athlete_service.get_athlete_by_id(athlete_id, session), 'nicht-gehashed'
    )
    assert response.status_code == 202, f' {str(response.status_code)}'
    assert response.json()['firstname'] == 'markus'
    assert response.json()['lastname'] == 'quarkus'
    assert response.json()['birthday'] is not None
    # Check that last_edited_at is a recent timestamp (within last minute)

    last_edited_str = response.json()['last_edited_at']
    # Simple check: just verify the date part matches today
    today = datetime.now().strftime('%Y-%m-%d')
    assert today in last_edited_str, (
        f"Last edited date {last_edited_str} should contain today's date {today}"
    )


def test_delete_athlete(client: TestClient, session: Session) -> None:
    # Create a trainer and athlete for this test
    trainer: Trainer = Trainer(
        username='trainer_for_delete',
        email='trainer_for_delete',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()

    athlete_body = {
        'username': 'test_athlete_for_delete',
        'email': 'test_delete@email.com',
        'unhashed_password': 'password',
        'firstname': 'test',
        'lastname': 'athlete',
        'birthday': '2024-02-18',
        'trainer_id': f'{trainer.id}',
        'gender': 'm',
    }

    # Create an athlete first
    create_response = client.post(
        '/athletes', json=athlete_body, headers=TestVariables.headers
    )
    assert create_response.status_code == 201
    athlete_id = create_response.json()['id']

    # Now test deleting the athlete
    response = client.delete(f'/athletes/{athlete_id}', headers=TestVariables.headers)
    assert response.status_code == 200, f' {str(response.status_code)}'
