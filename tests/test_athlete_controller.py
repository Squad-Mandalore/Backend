import pytest
from fastapi.openapi.models import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.models import Base
from tests.define_test_variables import client, TestVariables


@pytest.fixture
def session():
    # Replace the connection string with your actual database connection details.
    engine = create_engine("sqlite:///db/test.db", echo=True, connect_args={"check_same_thread": False})
    # engine = create_engine("sqlite:///db/test_test.db", echo=True, connect_args={"check_same_thread": False})

    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


def post_athlete(username: str, client) -> Response:
    body = {
        "username": username,
        "email": "ole@mail",
        "unhashed_password": "nicht-gehashed",
        "firstname": "ole",
        "lastname": "grundmann",
        "birthday": "2024-02-18",
        "trainer_id": "16d094b1-e9cf-4cf4-b3ea-6a832582adf2",
        "has_disease": True,
        "gender": "m"
    }
    response: Response = client.post(TestVariables.BASEURL + "/athletes", json=body, headers=TestVariables.HEADERS)
    assert response.status_code == 201, f" {str(response.status_code)}: {str(response.content)}"
    return response


def test_get_all_athletes(client, session) -> None:
    post_athlete("user420", client)
    response = client.get(TestVariables.BASEURL + "/athletes/all", headers=TestVariables.HEADERS)
    assert response.status_code == 200, f" {str(response.status_code)}: {str(response.content)}"


def test_get_athlete_by_id(client, session) -> None:
    postResponse: Response = post_athlete("user100", client)
    id: str = postResponse.json()['id']
    response = client.get(TestVariables.BASEURL + f"/athletes/{id}", headers=TestVariables.HEADERS)
    assert response.status_code == 200, f" {str(response.status_code)}: {str(response.content)} athlete id is: {id}"
    assert response.json()['username'] == "user100"


def test_delete_athlete(client, session) -> None:
    postResponse: Response = post_athlete("user55", client)
    id: str = str(postResponse.json()[id])
    response = client.delete(TestVariables.BASEURL + f"/athletes/{id}", headers=TestVariables.HEADERS)
    assert response.status_code == 200, f" {str(response.status_code)}: {str(response.content)}"


def test_post_athlete(client, session) -> None:
    response: Response = post_athlete("user69", client)
    assert response.status_code == 201


def test_put_athlete(client, session) -> None:
    postResponse: Response = post_athlete('user7', client)
    id: str = postResponse.json()['id']
    body = {
        "firstname": "markus",
        "lastname": "quarkus"
    }
    response = client.put(TestVariables.BASEURL + f"/athletes/{id}", json=body, headers=TestVariables.HEADERS)
    athlete = client.get(TestVariables.BASEURL + f"/athletes/{id}", headers=TestVariables.HEADERS)
    assert athlete.json()["firstname"] == "markus"
    assert athlete.json()["lastname"] == "quarkus"
