from fastapi.testclient import TestClient
from httpx import Response
from sqlalchemy.orm import Session

from src.models.models import Category, Exercise
from tests.define_test_variables import TestVariables, client_fixture, session_fixture

client = client_fixture
session = session_fixture

def test_create_rule(session: Session, client: TestClient) -> None:
    # create a category first
    category = Category(title="Ausdauer")
    session.add(category)
    session.flush()
    # create an exercise
    exercise = Exercise(title="title", from_age=12, to_age=18, category_id=category.id)
    session.add(exercise)
    session.commit()
    body = {
        "gender": "f",
        "from_age": 12,
        "to_age": 18,
        "bronze": "2",
        "silver": "3",
        "gold": "1",
        "year": "2007-01-01",
        "exercise_id": exercise.id
    }
    response: Response = client.post("/rules", json=body, headers=TestVariables.headers)
    assert response.status_code == 201, f"{str(response.status_code)} {response.json()}"
    assert response.json()["gender"] == "f"
    assert response.json()["from_age"] == 12
    assert response.json()["to_age"] == 18
    assert response.json()["bronze"] == "2"
    assert response.json()["silver"] == "3"
    assert response.json()["gold"] == "1"
    assert response.json()["year"] == "2007-01-01"

def test_get_all_rules(client: TestClient):
    response = client.get("/rules", headers=TestVariables.headers)
    TestVariables.test_rule = response.json()[0]

    assert response.status_code == 200, f"{str(response.status_code)} {response.json()}"

def test_get_rule_by_id(client: TestClient):
    rule_id = TestVariables.test_rule['id']
    response = client.get(f"/rules/{rule_id}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()["gender"] == "f"
    assert response.json()["from_age"] == 12
    assert response.json()["to_age"] == 18
    assert response.json()["bronze"] == "2"
    assert response.json()["silver"] == "3"
    assert response.json()["gold"] == "1"
    assert response.json()["year"] == "2007-01-01"

def test_patch_rule(client: TestClient) -> None:
    rule_id = TestVariables.test_rule['id']
    body = {
        "bronze": "1",
        "silver": "2",
        "gold": "3",
    }
    response: Response = client.patch(f"/rules/{rule_id}", json=body, headers=TestVariables.headers)
    assert response.status_code == 202, f"{str(response.status_code)} {response.json()}"
    assert response.json()["bronze"] == "1"
    assert response.json()["silver"] == "2"
    assert response.json()["gold"] == "3"

def test_delete_rule(client: TestClient) -> None:
    rule_id = TestVariables.test_rule['id']
    response = client.delete(f"/rules/{rule_id}", headers=TestVariables.headers)
    assert response.status_code == 200, f"{str(response.status_code)} {response.json()}"
