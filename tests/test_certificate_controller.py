
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from src.models.models import Certificate
from tests.define_test_variables import TestVariables


def test_post_certificate(session: Session, client: TestClient):
    test_blob = b'"HalloWelt"'
    certificate: Certificate = Certificate(athlete_id="CHUCHUID", uploader="admin", title="HansNachweis", blob=test_blob)

    session.add(certificate)
    session.commit()
    certificate_new = session.query(Certificate).filter(Certificate.title == "HansNachweis").first()
    if certificate_new is None:
        assert False, 'Certificate not found'

    body = {
        ''
    }

    response = client.post('/certificates', json=body, headers=TestVariables.headers)
    assert response.status_code == 201, f"{response.status_code} {response.json()}"

def test_get_all_certificates(client: TestClient):
    response = client.get("/certificates", headers=TestVariables.headers)
    TestVariables.test_athlete = response.json()[0]

    assert response.status_code == 200, f" {str(response.status_code)}"

def test_get_certificate_by_id(client: TestClient):
    certificate_id = TestVariables.test_certificate['id']
    response = client.get(f"/certificates/{certificate_id}", headers=TestVariables.headers)
    assert response.status_code == 200
    assert response.json()['title'] == "title"

def test_delete_certificate(client: TestClient) -> None:
    certificate_id = TestVariables.test_certificate['id']
    response = client.delete(f"/athletes/{certificate_id}", headers=TestVariables.headers)
    assert response.status_code == 200, f" {str(response.status_code)}"


