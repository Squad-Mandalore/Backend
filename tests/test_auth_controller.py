from fastapi.testclient import TestClient

from tests.define_test_variables import TestVariables


def test_login(client: TestClient):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    body = 'grant_type=password&username=admin&password=admin123'

    response = client.post('/auth/login', headers=headers, content=body)
    assert response.status_code == 200, f'{response.status_code}'
    assert response.json()['access_token'] != ''
    assert response.json()['refresh_token'] != ''
    TestVariables.access_token = response.json()['access_token']
    TestVariables.refresh_token = response.json()['refresh_token']


def test_refresh(client: TestClient):
    # First login to get a refresh token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    body = 'grant_type=password&username=admin&password=admin123'
    login_response = client.post('/auth/login', headers=headers, content=body)
    assert login_response.status_code == 200

    refresh_token = login_response.json()['refresh_token']

    # Now test refresh
    refresh_headers = {'x-refresh-token': refresh_token}
    response = client.post('/auth/refresh', headers=refresh_headers)
    assert response.status_code == 200, f'{response.status_code}'
    assert response.json()['access_token'] != ''
    assert response.json()['refresh_token'] != ''


def test_who_am_i(client: TestClient):
    response = client.get('/auth/whoami', headers=TestVariables.headers)
    assert response.status_code == 200, f'{response.status_code}'
    assert response.json()['username'] != ''
