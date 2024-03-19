from fastapi.testclient import TestClient

from tests.define_test_variables import TestVariables, client_fixture, session_fixture

def test_login(client: TestClient):
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    body = 'grant_type=password&username=init&password=admin'

    response = client.post("/auth/login", headers=headers, content=body)
    assert response.status_code == 200, f"{response.status_code}"
    assert response.json()['access_token'] != ''
    assert response.json()['refresh_token'] != ''
    TestVariables.access_token = response.json()['access_token']
    TestVariables.refresh_token = response.json()['refresh_token']

def test_refresh(client: TestClient):
    headers = { 'x-refresh-token': TestVariables.refresh_token }
    response = client.post("/auth/refresh", headers=headers)
    assert response.status_code == 200, f"{response.status_code}"
    assert response.json()['access_token'] != ''
    assert response.json()['refresh_token'] != ''
    TestVariables.access_token = response.json()['access_token']
    TestVariables.refresh_token = response.json()['refresh_token']
