from datetime import datetime
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from src.models.models import Certificate, Athlete, Trainer, Gender
from tests.define_test_variables import TestVariables, session_fixture, client_fixture
from src.logger.logger import logger


def test_post_certificate(session: Session, client: TestClient):
    trainer: Trainer = Trainer(username="trainer", email="trainer", unhashed_password="trainer", firstname="trainer",
                               lastname="trainer")
    session.add(trainer)
    session.flush()
    athlete: Athlete = Athlete(username="username", email="ole@mail", unhashed_password="unhashed", firstname="ole",
                               lastname="grundmann", birthday=datetime.now(), trainer_id=trainer.id, gender=Gender.MALE)
    session.add(athlete)
    session.commit()

    data = {
        "athlete_id": f"{athlete.id}",
        "title": "Rettungsschwimmer12345",
    }
    files = {"blob": ("certificate.pdf", b"dummy_blob_content")}

    response = client.post('/certificates', files=files, data=data, headers=TestVariables.headers)
    assert response.status_code == 201, f"{response.status_code} {response.json()}"
    TestVariables.test_certificate = response.json()


def test_get_certificate_by_id(client: TestClient):
    certificate_id = TestVariables.test_certificate['id']
    response = client.get(f"/certificates/{certificate_id}", headers=TestVariables.headers)
    assert response.status_code == 200


def test_delete_certificate(client: TestClient):
    certificate_id = TestVariables.test_certificate['id']
    logger.warning(f"Deleting certificate with id {certificate_id}")
    response = client.delete(f"/certificates/{certificate_id}", headers=TestVariables.headers)
    assert response.status_code == 200, f'{str(response.status_code)} {response.json()}'
