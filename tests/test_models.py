from datetime import date, datetime
from sqlalchemy.exc import InvalidRequestError

import pytest
from src.models import models
from tests.define_test_variables import session_fixture

def test_user(session):
    with pytest.raises(InvalidRequestError):
        user = models.User(username="test", email="test", unhashed_password="test", firstname="test", lastname="test")
        session.add(user)
        session.commit()

def test_admin(session):
    admin = models.Administrator(username="admin", email="admin", unhashed_password="admin", firstname="admin", lastname="admin", uses_otp=False)
    session.add(admin)
    session.commit()
    admin = session.query(models.Administrator).filter(models.Administrator.username == "admin").first()

    assert admin.id is not None
    assert admin.username == "admin"
    assert admin.email == "admin"

def test_trainer(session):
    trainer = models.Trainer(username="trainer", email="trainer", unhashed_password="trainer", firstname="trainer", lastname="trainer", uses_otp=False, birthday=None)
    session.add(trainer)
    session.commit()
    trainer = session.query(models.Trainer).filter(models.Trainer.username == "trainer").first()

    assert trainer.id is not None
    assert trainer.username == "trainer"
    assert trainer.email == "trainer"


def test_athlete(session):
    trainer = models.Trainer(username="trainer_athlete", email="trainer", unhashed_password="trainer", firstname="trainer", lastname="trainer",  uses_otp=False, birthday=None)
    session.add(trainer)
    session.commit()
    trainerDb = session.query(models.Trainer).filter(models.Athlete.username == "trainer_athlete").first()
    athlete = models.Athlete(username="athlete", email="athlete", unhashed_password="athlete", firstname="athlete", lastname="athlete",  birthday=date.today(), gender=models.Gender.DIVERSE, has_disease=False, trainer_id=trainerDb.id)
    session.add(athlete)
    session.commit()
    athlete = session.query(models.Athlete).filter(models.Athlete.username == "athlete").first()

    assert athlete.id is not None
    assert athlete.username == "athlete"
    assert athlete.email == "athlete"
    assert athlete.trainer_id == trainer.id
    assert trainer.athletes[0] == athlete

def test_category(session):
    category = models.Category(title="category")
    session.add(category)
    session.commit()
    category = session.query(models.Category).filter(models.Category.title == "category").first()

    assert category.id is not None
    assert category.title == "category"

def test_certificate(session):
    trainer = models.Trainer(username="trainer_athlete_certificate", email="trainer", unhashed_password="trainer", firstname="trainer", lastname="trainer",  uses_otp=False, birthday=None)
    session.add(trainer)
    session.commit()
    trainerDb = session.query(models.Trainer).filter(models.Athlete.username == "trainer_athlete_certificate").first()
    athlete = models.Athlete(username="athlete_certificate", email="athlete", unhashed_password="athlete", firstname="athlete", lastname="athlete",  birthday=date.today(), gender=models.Gender.DIVERSE, has_disease=False, trainer_id=trainerDb.id)
    session.add(athlete)
    session.commit()
    athleteDb = session.query(models.Athlete).filter(models.Athlete.username == "athlete_certificate").first()
    certificate = models.Certificate(title="certificate", blob=b"blob", athlete_id=athleteDb.id, uploader=trainerDb.id)
    session.add(certificate)
    session.commit()
    certificate = session.query(models.Certificate).filter(models.Certificate.title == "certificate").first()

    assert certificate.id is not None
    assert certificate.title == "certificate"
    assert certificate.blob == b"blob"
    assert certificate.athlete == athlete
    assert certificate.uploader == trainer
    assert athlete.certificates[0] == certificate

def test_code_administrator(session):
    admin = models.Administrator(username="admin_code", email="admin", unhashed_password="admin", firstname="admin", lastname="admin", uses_otp=False)
    session.add(admin)
    session.commit()
    adminDb = session.query(models.Administrator).filter(models.Administrator.username == "admin_code").first()
    code = models.BackupCode(code="test_admin", user_id=adminDb.id)
    session.add(code)
    session.commit()
    code = session.query(models.BackupCode).filter(models.BackupCode.code == "test_admin").first()

    assert code.user_id is not None
    assert code.code == "test_admin"
    assert code.administrator == admin
    assert admin.codes[0] == code

def test_code_trainer(session):
    trainer = models.Trainer(username="trainer_code", email="trainer", unhashed_password="trainer", firstname="trainer", lastname="trainer", uses_otp=False, birthday=None)
    session.add(trainer)
    session.commit()
    trainerDb = session.query(models.Trainer).filter(models.Trainer.username == "trainer_code").first()
    code = models.BackupCode(code="test_trainer", user_id=trainerDb.id)
    session.add(code)
    session.commit()
    code = session.query(models.BackupCode).filter(models.BackupCode.code == "test_trainer").first()

    assert code.user_id is not None
    assert code.code == "test_trainer"
    assert code.trainer == trainer
    assert trainer.codes[0] == code

def test_exercise(session):
    category = models.Category(title="category_exercise")
    session.add(category)
    session.commit()
    categoryDb = session.query(models.Category).filter(models.Category.title == "category_exercise").first()
    exercise = models.Exercise(title="exercise", category_id=categoryDb.id, from_age=10, to_age=20)
    session.add(exercise)
    session.commit()
    exercise = session.query(models.Exercise).filter(models.Exercise.title == "exercise").first()

    assert exercise.id is not None
    assert exercise.title == "exercise"
    assert exercise.category == category

def test_completes(session):
    trainer = models.Trainer(username="trainer_athlete_completes", email="trainer", unhashed_password="trainer", firstname="trainer", lastname="trainer", uses_otp=False, birthday=None)
    session.add(trainer)
    session.commit()
    trainerDb = session.query(models.Trainer).filter(models.Athlete.username == "trainer_athlete_completes").first()
    athlete = models.Athlete(username="athlete_completes", email="athlete", unhashed_password="athlete", firstname="athlete", lastname="athlete",  birthday=date.today(), gender=models.Gender.DIVERSE, has_disease=False, trainer_id=trainerDb.id)
    session.add(athlete)
    session.commit()
    athleteDb = session.query(models.Athlete).filter(models.Athlete.username == "athlete_completes").first()
    category = models.Category(title="category_exercise_completes")
    session.add(category)
    session.commit()
    categoryDb = session.query(models.Category).filter(models.Category.title == "category_exercise_completes").first()
    exercise = models.Exercise(title="exercise_completes", category_id=categoryDb.id, from_age=10, to_age=20)
    session.add(exercise)
    session.commit()
    exerciseDb = session.query(models.Exercise).filter(models.Exercise.title == "exercise_completes").first()
    completes = models.Completes(athlete_id=athleteDb.id, exercise_id=exerciseDb.id, tracked_at=datetime.now(), completed_at=datetime.now(), result="result", points=1)
    session.add(completes)
    session.commit()
    completes = session.query(models.Completes).filter(models.Completes.result == "result").first()

    assert completes.exercise == exercise
    assert completes.athlete == athlete
    assert completes.result == "result"
    assert athlete.completes[0].exercise == exercise
