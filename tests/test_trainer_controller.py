from datetime import datetime

from fastapi.testclient import TestClient
from httpx import Response

from tests.define_test_variables import client_fixture
from tests.define_test_variables import session_fixture
from tests.define_test_variables import TestVariables


client = client_fixture
session = session_fixture


def test_post_trainer(client: TestClient):
    body = {
        'username': 'username',
        'email': 'ole@mail',
        'unhashed_password': 'nicht-gehashed',
        'firstname': 'ole',
        'lastname': 'grundmann',
    }
    response = client.post('/trainers', json=body, headers=TestVariables.headers)
    assert response.status_code == 201, f'{response.status_code} {response.json()}'


def test_get_all_trainers(client: TestClient):
    response = client.get('/trainers', headers=TestVariables.headers)
    TestVariables.test_trainer = response.json()[1]

    assert response.status_code == 200, f' {response.status_code!s}'


def test_get_trainer_by_id(client: TestClient):
    trainer_id = TestVariables.test_trainer['id']
    response = client.get(f'/trainers/{trainer_id}', headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()['username'] == 'username'


def test_patch_trainer(client: TestClient) -> None:
    trainer_id = TestVariables.test_trainer['id']
    body = {'firstname': 'markus', 'lastname': 'quarkus'}
    response: Response = client.patch(
        f'/trainers/{trainer_id}', json=body, headers=TestVariables.headers
    )
    assert response.status_code == 202, f' {response.status_code!s}'
    assert response.json()['firstname'] == 'markus'
    assert response.json()['lastname'] == 'quarkus'
    assert (
        response.json()['last_edited_at'][:-6]
        == datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-6]
    )


def test_delete_trainer(client: TestClient) -> None:
    trainer_id = TestVariables.test_trainer['id']
    response = client.delete(f'/trainers/{trainer_id}', headers=TestVariables.headers)
    assert response.status_code == 200, f' {response.status_code!s}'
