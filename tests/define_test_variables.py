from os import getenv
from typing import cast

from fastapi import Depends
from fastapi.testclient import TestClient
import jwt
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from src.database.database_utils import get_by_id, get_db
from src.main import app
from src.models.models import Base, User
from src.services.auth_service import ALGORITHM, get_current_user, oauth2_bearer

# Description: This file contains the test variables that are used in the test cases

class TestVariables():
    HEADERS: dict = {'content-type': 'application/json', 'authorization':''}
    BASEURL: str = 'http://127.0.0.1:8000'
    EXAMPLE_PASSWORD: dict = {"password": "Go is the GOAT"}

@pytest.fixture(name="session", scope="session")
def session_fixture():
    engine = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    def get_current_user_override(token: str = Depends(oauth2_bearer)):
        payload = jwt.decode(token, getenv('JWT_KEY', 'test'), algorithms=[ALGORITHM], options={"verify_exp": False, "verify_signature": False})
        user = get_by_id(User, payload["user_id"], get_session_override())
        return cast(User, user)

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    client = TestClient(app)
    response = client.post(
        "/auth/login",
        data={"username": "init", "password": "admin"},
    )
    TestVariables.HEADERS['authorization'] = f'Bearer {response.json()["access_token"]}'
    yield client
    app.dependency_overrides.clear()
