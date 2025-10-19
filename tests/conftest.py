import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.main import app
from src.models.models import Administrator, Base, User
from src.services.auth_service import get_current_user


class TestVariables:
    BASEURL: str = 'http://127.0.0.1:8000'
    headers: dict = {}
    access_token: str
    refresh_token: str
    test_athlete: dict = {}
    test_trainer: dict = {}
    test_exercise: dict = {}
    test_completes: dict = {}
    test_category: dict = {}
    test_certificate: dict = {}
    test_rule: dict = {}
    test_admin: dict = {}


@pytest.fixture(name='session', scope='function')
def session_fixture():
    engine = create_engine(
        'sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        admin = Administrator(
            username='admin',
            unhashed_password='admin123',
            email='admin',
            firstname='admin',
            lastname='admin',
        )
        session.add(admin)
        session.commit()
        yield session


@pytest.fixture(name='class_session', scope='class')
def class_session_fixture():
    """Session fixture with class scope for tests that need to share data within a test class"""
    engine = create_engine(
        'sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        admin = Administrator(
            username='admin',
            unhashed_password='admin123',
            email='admin',
            firstname='admin',
            lastname='admin',
        )
        session.add(admin)
        session.commit()
        yield session


@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_session_override():
        return session

    def get_current_user_override():
        # Just return the admin user we created in the session fixture
        admin_user = session.query(User).filter(User.username == 'admin').first()
        return admin_user

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    client = TestClient(app)
    # We don't need to login since we override get_current_user
    TestVariables.headers = {}  # No authorization needed since we override auth
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name='mock_file')
def mock_file_fixture(tmp_path):
    """Create a temporary file for testing."""
    file_path = tmp_path / 'test_file.txt'
    file_path.write_text('test content')
    return str(file_path)
