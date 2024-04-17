from datetime import datetime

from fastapi.testclient import TestClient
from httpx import Response
from src.services import password_service, admin_service
from tests.define_test_variables import TestVariables, client_fixture, session_fixture

client = client_fixture
session = session_fixture

#def test_post_admin(client: TestClient):
#    body = {
#        "username": "admin_test",
#        "email": "admin",
#        "unhashed_password": "nicht-gehashed",
#        "firstname": "admin",
#        "lastname": "admin",
#    }
#    response = client.post("/admins", json=body, headers=TestVariables.headers)
#    assert response.status_code == 201, f"{response.status_code} {response.json()}"

def test_get_all_admins(client: TestClient):
    response = client.get("/admins", headers=TestVariables.headers)
    TestVariables.test_admin = response.json()[0]

    assert response.status_code == 200, f" {str(response.status_code)}"

def test_get_admin_by_id(client: TestClient):
    admin_id = TestVariables.test_admin['id']
    response = client.get(f"/admins/{admin_id}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()['username'] == "admin"

def test_patch_admin(client: TestClient, session) -> None:
    admin_id = TestVariables.test_admin['id']
    body = {
        "firstname": "admin_updated",
        "lastname": "admin_updated_last",
        "unhashed_password": "TEST"
    }
    response: Response = client.patch(f"/admins/{admin_id}", json=body, headers=TestVariables.headers)

    assert True == password_service.verify_password(admin_service.get_admin_by_id(admin_id, session), body["unhashed_password"])
    assert response.status_code == 202, f" {str(response.status_code)}"
    assert response.json()["firstname"] == "admin_updated"
    assert response.json()["lastname"] == "admin_updated_last"
    assert response.json()["last_edited_at"][:-6] == datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-6]
    assert response.json()["last_password_change"][:-6] == datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-6]

#def test_delete_admin(client: TestClient) -> None:
#    admin_id = TestVariables.test_admin['id']
#    response = client.delete(f"/admins/{admin_id}", headers=TestVariables.headers)
#    assert response.status_code == 200, f" {str(response.status_code)}"
