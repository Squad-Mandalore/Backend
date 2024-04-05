from datetime import datetime

from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

#client_fixture, session_fixture are fixtures that are used to create a test client and a session for the test cases !!DO NOT REMOVE!!
from src.models.models import Trainer
from tests.define_test_variables import TestVariables, client_fixture, session_fixture

def test_post_athlete(session: Session, client: TestClient):
    trainer: Trainer = Trainer(username="trainer", email="trainer", unhashed_password="trainer", firstname="trainer", lastname="trainer")
    session.add(trainer)
    session.commit()
    trainer_new = session.query(Trainer).filter(Trainer.username == "trainer").first()
    if trainer_new is None:
        assert False, "Trainer not found"

    body = {
        "username": "username",
        "email": "ole@mail",
        "unhashed_password": "nicht-gehashed",
        "firstname": "ole",
        "lastname": "grundmann",
        "birthday": "2024-02-18",
        "trainer_id": f"{trainer_new.id}",
        "gender": "m"
    }

    response = client.post("/athletes", json=body, headers=TestVariables.headers)
    assert response.status_code == 201, f"{response.status_code} {response.json()}"

def test_get_all_athletes(client: TestClient):
    response = client.get("/athletes", headers=TestVariables.headers)
    TestVariables.test_athlete = response.json()[0]

    assert response.status_code == 200, f" {str(response.status_code)}"

def test_get_athlete_by_id(client: TestClient):
    athlete_id = TestVariables.test_athlete['id']
    response = client.get(f"/athletes/{athlete_id}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()['username'] == "username"

def test_get_full_athlete_by_id(client: TestClient):
    athlete_id = TestVariables.test_athlete['id']
    response = client.get(f"/athletes/{athlete_id}/full", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()['username'] == "username"

def test_patch_athlete(client: TestClient) -> None:
    athlete_id = TestVariables.test_athlete['id']
    body = {
        "firstname": "markus",
        "lastname": "quarkus"
    }
    response: Response = client.patch(f"/athletes/{athlete_id}", json=body, headers=TestVariables.headers)
    assert response.status_code == 202, f" {str(response.status_code)}"
    assert response.json()["firstname"] == "markus"
    assert response.json()["lastname"] == "quarkus"
    assert response.json()["birthday"] is not None
    assert response.json()["last_edited_at"][:-6] == datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-6]

def test_delete_athlete(client: TestClient) -> None:
    athlete_id = TestVariables.test_athlete['id']
    response = client.delete(f"/athletes/{athlete_id}", headers=TestVariables.headers)
    assert response.status_code == 200, f" {str(response.status_code)}"
