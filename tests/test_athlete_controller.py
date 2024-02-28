from datetime import datetime

from httpx import Response

from tests.define_test_variables import TestVariables, client

testUser = {}

def test_post_athlete():
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
    response = client.post(TestVariables.BASEURL + "/athletes", json=body, headers=TestVariables.HEADERS)
    assert response.status_code == 201, f"{response.status_code}"

def test_get_all_athletes():
    response = client.get(TestVariables.BASEURL + "/athletes/all", headers=TestVariables.HEADERS)
    global testUser
    testUser = response.json()[0]
    assert response.status_code == 200, f" {str(response.status_code)}"

def test_get_athlete_by_id():
    idtoll = testUser['id']
    response = client.get(TestVariables.BASEURL + f"/athletes/{idtoll}", headers=TestVariables.HEADERS)
    assert response.status_code == 200
    assert response.json()['username'] == "username"

def test_put_athlete() -> None:
    idtoll = testUser['id']
    body = {
        "firstname": "markus",
        "lastname": "quarkus"
    }
    response: Response = client.put(TestVariables.BASEURL + f"/athletes/{idtoll}", json=body, headers=TestVariables.HEADERS)
    assert response.status_code == 202, f" {str(response.status_code)}"
    assert response.json()["firstname"] == "markus"
    assert response.json()["lastname"] == "quarkus"
    assert response.json()["birthday"] is not None
    assert response.json()["last_edited_at"] == datetime.now().strftime("%Y-%m-%d %H:%M")

def test_delete_athlete() -> None:
    idtoll = testUser['id']
    response = client.delete(TestVariables.BASEURL + f"/athletes/{idtoll}", headers=TestVariables.HEADERS)
    assert response.status_code == 200, f" {str(response.status_code)}"
