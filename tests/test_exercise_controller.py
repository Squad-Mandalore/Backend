from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

from src.models.models import Category
from tests.define_test_variables import TestVariables, client_fixture, session_fixture

client = client_fixture
session = session_fixture

def test_create_exercise(session: Session, client: TestClient) -> None:
    # create a category first
    category = Category(title="Ausdauer")
    session.add(category)
    session.commit()
    body = {
        "title": "title",
        "category_id": category.id
    }
    response: Response = client.post("/exercises", json=body, headers=TestVariables.headers)
    assert response.status_code == 201, f"{str(response.status_code)} {response.json()}"
    assert response.json()["title"] == "title"

def test_get_all_exercises(client: TestClient):
    response = client.get("/exercises", headers=TestVariables.headers)
    TestVariables.test_exercise = response.json()[0]

    assert response.status_code == 200, f"{str(response.status_code)} {response.json()}"

def test_get_exercise_by_id(client: TestClient):
    exercise_id = TestVariables.test_exercise['id']
    response = client.get(f"/exercises/{exercise_id}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()['title'] == "title"

def test_patch_exercise(client: TestClient) -> None:
    exercise_id = TestVariables.test_exercise['id']
    body = {
        "title": "markus",
    }
    response: Response = client.patch(f"/exercises/{exercise_id}", json=body, headers=TestVariables.headers)
    assert response.status_code == 202, f"{str(response.status_code)} {response.json()}"
    assert response.json()["title"] == "markus"

def test_delete_exercise(client: TestClient) -> None:
    exercise_id = TestVariables.test_exercise['id']
    response = client.delete(f"/exercises/{exercise_id}", headers=TestVariables.headers)
    assert response.status_code == 200, f"{str(response.status_code)} {response.json()}"
