from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.logger.logger import logger
from src.models.models import Athlete
from src.models.models import Gender
from src.models.models import Trainer

from tests.define_test_variables import TestVariables


def test_post_certificate(session: Session, client: TestClient):
    trainer: Trainer = Trainer(
        username='trainer',
        email='trainer',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.flush()
    athlete: Athlete = Athlete(
        username='username',
        email='ole@mail',
        unhashed_password='unhashed',
        firstname='ole',
        lastname='grundmann',
        birthday=datetime.now(),
        trainer_id=trainer.id,
        gender=Gender.MALE,
    )
    session.add(athlete)
    session.commit()

    data = {
        'athlete_id': f'{athlete.id}',
        'title': 'Rettungsschwimmer12345',
    }
    files = {'blob': ('certificate.pdf', b'dummy_blob_content')}

    response = client.post(
        '/certificates', files=files, data=data, headers=TestVariables.headers
    )
    assert response.status_code == 201, f'{response.status_code} {response.json()}'


def test_get_certificate_by_id(session: Session, client: TestClient):
    # Create trainer and athlete for this test
    trainer: Trainer = Trainer(
        username='trainer2',
        email='trainer2@email.com',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.flush()
    athlete: Athlete = Athlete(
        username='athlete2',
        email='athlete2@mail.com',
        unhashed_password='unhashed',
        firstname='ole',
        lastname='grundmann',
        birthday=datetime.now(),
        trainer_id=trainer.id,
        gender=Gender.MALE,
    )
    session.add(athlete)
    session.commit()

    # Create certificate for this test
    data = {
        'athlete_id': f'{athlete.id}',
        'title': 'Rettungsschwimmer12345',
    }
    files = {'blob': ('certificate.pdf', b'dummy_blob_content')}

    create_response = client.post(
        '/certificates', files=files, data=data, headers=TestVariables.headers
    )
    assert create_response.status_code == 201
    certificate_id = create_response.json()['id']

    # Now test getting the certificate
    response = client.get(
        f'/certificates/{certificate_id}', headers=TestVariables.headers
    )
    assert response.status_code == 200


def test_delete_certificate(session: Session, client: TestClient):
    # Create trainer and athlete for this test
    trainer: Trainer = Trainer(
        username='trainer3',
        email='trainer3@email.com',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.flush()
    athlete: Athlete = Athlete(
        username='athlete3',
        email='athlete3@mail.com',
        unhashed_password='unhashed',
        firstname='ole',
        lastname='grundmann',
        birthday=datetime.now(),
        trainer_id=trainer.id,
        gender=Gender.MALE,
    )
    session.add(athlete)
    session.commit()

    # Create certificate for this test
    data = {
        'athlete_id': f'{athlete.id}',
        'title': 'Rettungsschwimmer12345',
    }
    files = {'blob': ('certificate.pdf', b'dummy_blob_content')}

    create_response = client.post(
        '/certificates', files=files, data=data, headers=TestVariables.headers
    )
    assert create_response.status_code == 201
    certificate_id = create_response.json()['id']

    # Now test deleting the certificate
    logger.warning(f'Deleting certificate with id {certificate_id}')
    response = client.delete(
        f'/certificates/{certificate_id}', headers=TestVariables.headers
    )
    assert response.status_code == 200, f'{response.status_code!s} {response.json()}'
