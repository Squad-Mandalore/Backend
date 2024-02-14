from datetime import date, datetime
from sqlalchemy.exc import InvalidRequestError

import pytest
from src.models.models import *

@pytest.fixture
def session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Replace the connection string with your actual database connection details.
    engine = create_engine("sqlite:///:memory:", echo=True, connect_args={"check_same_thread": False})
    #engine = create_engine("sqlite:///db/test_test.db", echo=True, connect_args={"check_same_thread": False})

    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

def test_user(session):
    with pytest.raises(InvalidRequestError):
        user = User(username="test", email="test", hashed_password="test", firstname="test", lastname="test", salt="test")
        session.add(user)
        session.commit()

def test_admin(session):
    admin = Administrator(username="admin", email="admin", hashed_password="admin", firstname="admin", lastname="admin", salt="admin", uses_otp=False)
    session.add(admin)
    session.commit()
    admin = session.query(Administrator).filter(Administrator.username == "admin").first()

    assert admin.id is not None
    assert admin.username == "admin"
    assert admin.email == "admin"
    assert admin.hashed_password == "admin"

def test_trainer(session):
    trainer = Trainer(username="trainer", email="trainer", hashed_password="trainer", firstname="trainer", lastname="trainer", salt="trainer", uses_otp=False, birthday=None)
    session.add(trainer)
    session.commit()
    trainer = session.query(Trainer).filter(Trainer.username == "trainer").first()

    assert trainer.id is not None
    assert trainer.username == "trainer"
    assert trainer.email == "trainer"
    assert trainer.hashed_password == "trainer"

def test_athlete(session):
    trainer = Trainer(username="trainer_athlete", email="trainer", hashed_password="trainer", firstname="trainer", lastname="trainer", salt="trainer", uses_otp=False, birthday=None)
    athlete = Athlete(username="athlete", email="athlete", hashed_password="athlete", firstname="athlete", lastname="athlete", salt="athlete", birthday=date.today(), gender=Gender.DIVERSE, has_disease=False, trainer=trainer)
    session.add(athlete)
    session.commit()
    athlete = session.query(Athlete).filter(Athlete.username == "athlete").first()

    assert athlete.id is not None
    assert athlete.username == "athlete"
    assert athlete.email == "athlete"
    assert athlete.hashed_password == "athlete"
    assert athlete.trainer == trainer
    assert trainer.athletes[0] == athlete

def test_category(session):
    category = Category(title="category")
    session.add(category)
    session.commit()
    category = session.query(Category).filter(Category.title == "category").first()

    assert category.id is not None
    assert category.title == "category"

def test_certificate(session):
    trainer = Trainer(username="trainer_athlete_certificate", email="trainer", hashed_password="trainer", firstname="trainer", lastname="trainer", salt="trainer", uses_otp=False, birthday=None)
    athlete = Athlete(username="athlete_certificate", email="athlete", hashed_password="athlete", firstname="athlete", lastname="athlete", salt="athlete", birthday=date.today(), gender=Gender.DIVERSE, has_disease=False, trainer=trainer)
    certificate = Certificate(title="certificate", blob=b"blob", athlete=athlete, uploader=trainer)
    session.add(certificate)
    session.commit()
    certificate = session.query(Certificate).filter(Certificate.title == "certificate").first()

    assert certificate.id is not None
    assert certificate.title == "certificate"
    assert certificate.blob == b"blob"
    assert certificate.athlete == athlete
    assert certificate.uploader == trainer
    assert athlete.certificates[0] == certificate

def test_code_administrator(session):
    admin = Administrator(username="admin_code", email="admin", hashed_password="admin", firstname="admin", lastname="admin", salt="admin", uses_otp=False)
    code = BackupCode(code="test_admin", user=admin)
    session.add(code)
    session.commit()
    code = session.query(BackupCode).filter(BackupCode.code == "test_admin").first()

    assert code.user_id is not None
    assert code.code == "test_admin"
    assert code.administrator == admin
    assert admin.codes[0] == code

def test_code_trainer(session):
    trainer = Trainer(username="trainer_code", email="trainer", hashed_password="trainer", firstname="trainer", lastname="trainer", salt="trainer", uses_otp=False, birthday=None)
    code = BackupCode(code="test_trainer", user=trainer)
    session.add(code)
    session.commit()
    code = session.query(BackupCode).filter(BackupCode.code == "test_trainer").first()

    assert code.user_id is not None
    assert code.code == "test_trainer"
    assert code.trainer == trainer
    assert trainer.codes[0] == code

def test_exercise(session):
    category = Category(title="category_exercise")
    exercise = Exercise(title="exercise", category=category, from_age=10, to_age=20)
    session.add(exercise)
    session.commit()
    exercise = session.query(Exercise).filter(Exercise.title == "exercise").first()

    assert exercise.id is not None
    assert exercise.title == "exercise"
    assert exercise.category == category

def test_completes(session):
    trainer = Trainer(username="trainer_athlete_completes", email="trainer", hashed_password="trainer", firstname="trainer", lastname="trainer", salt="trainer", uses_otp=False, birthday=None)
    athlete = Athlete(username="athlete_completes", email="athlete", hashed_password="athlete", firstname="athlete", lastname="athlete", salt="athlete", birthday=date.today(), gender=Gender.DIVERSE, has_disease=False, trainer=trainer)
    category = Category(title="category_exercise_completes")
    exercise = Exercise(title="exercise_completes", category=category, from_age=10, to_age=20)
    completes = Completes(athlete=athlete, exercise=exercise, tracked_at=datetime.now(), completed_at=datetime.now(), result="result", points=1)
    session.add(completes)
    session.commit()
    completes = session.query(Completes).filter(Completes.result == "result").first()

    assert completes.exercise == exercise
    assert completes.athlete == athlete
    assert completes.result == "result"
    assert athlete.completes[0].exercise == exercise
