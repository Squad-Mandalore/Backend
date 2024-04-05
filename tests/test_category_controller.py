from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.values import parse_values
from tests.define_test_variables import TestVariables, client_fixture, session_fixture

client = client_fixture
session = session_fixture

def test_get_all_categories(session: Session, client: TestClient):
    parse_values(session)
    response = client.get("/categories", headers=TestVariables.headers)
    TestVariables.test_category = response.json()[0]
    # check if there are 4 categories in the response
    assert len(response.json()) == 4

    assert response.status_code == 200, f" {str(response.status_code)}"

def test_get_category_by_id(client: TestClient):
    category_id = TestVariables.test_category['id']
    response = client.get(f"/categories/{category_id}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()['title'] == "Ausdauer"
