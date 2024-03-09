from datetime import datetime

from fastapi.testclient import TestClient
from httpx import Response

#client_fixture, session_fixture are fixtures that are used to create a test client and a session for the test cases !!DO NOT REMOVE!!
from tests.define_test_variables import TestVariables, client_fixture, session_fixture, token_fixture

def test_post_athlete(client: TestClient, token: str):
    body = {
        "username": "username",
        "email": "ole@mail",
        "unhashed_password": "nicht-gehashed",
        "firstname": "ole",
        "lastname": "grundmann",
        "birthday": "2024-02-18",
        "trainer_id": "16d094b1-e9cf-4cf4-b3ea-6a832582adf2",
        "has_disease": True,
        "gender": "m"
    }
    TestVariables.HEADERS['authorization'] = f'Bearer {token}'
    response = client.post(TestVariables.BASEURL + "/athletes", json=body, headers=TestVariables.HEADERS)
    assert response.status_code == 201, f"{response.status_code} {response.json()}"

def test_get_all_athletes(client: TestClient, token: str):
    TestVariables.HEADERS['authorization'] = f'Bearer {token}'
    response = client.get(TestVariables.BASEURL + "/athletes/all", headers=TestVariables.HEADERS)
    TestVariables.athlete = response.json()[0]

    assert response.status_code == 200, f" {str(response.status_code)}"

def test_get_athlete_by_id(client: TestClient, token: str):
    athlete_id = TestVariables.athlete['id']
    TestVariables.HEADERS['authorization'] = f'Bearer {token}'
    response = client.get(TestVariables.BASEURL + f"/athletes/{athlete_id}", headers=TestVariables.HEADERS)
    assert response.status_code == 200
    assert response.json()['username'] == "username"

def test_patch_athlete(client: TestClient,token: str) -> None:
    athlete_id = TestVariables.athlete['id']
    body = {
        "firstname": "markus",
        "lastname": "quarkus"
    }
    TestVariables.HEADERS['authorization'] = f'Bearer {token}'
    response: Response = client.patch(TestVariables.BASEURL + f"/athletes/{athlete_id}", json=body, headers=TestVariables.HEADERS)
    assert response.status_code == 202, f" {str(response.status_code)}"
    assert response.json()["firstname"] == "markus"
    assert response.json()["lastname"] == "quarkus"
    assert response.json()["birthday"] is not None
    assert response.json()["last_edited_at"][:-5] == datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-5]

def test_delete_athlete(client: TestClient, token: str) -> None:
    athlete_id = TestVariables.athlete['id']
    TestVariables.HEADERS['authorization'] = f'Bearer {token}'
    response = client.delete(TestVariables.BASEURL + f"/athletes/{athlete_id}", headers=TestVariables.HEADERS)
    assert response.status_code == 200, f" {str(response.status_code)}"
