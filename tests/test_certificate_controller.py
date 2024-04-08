
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from src.models.models import Certificate
from tests.define_test_variables import TestVariables


def test_post_certificate(session: Session, client: TestClient):
    certificate: Certificate = Certificate(athlete_id="CHUCHUID", uploader="admin", title="HansNachweis")
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