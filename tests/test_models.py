from datetime import date
from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError
from src.models import models
from src.models.values import parse_values


def test_user(session):
    with pytest.raises(InvalidRequestError):
        user = models.User(
            username='test',
            email='test',
            unhashed_password='test',
            firstname='test',
            lastname='test',
        )
        session.add(user)
        session.commit()


def test_admin(session):
    admin1 = models.Administrator(
        username='admin1',
        email='admin1',
        unhashed_password='admin1',
        firstname='admin1',
        lastname='admin1',
    )
    session.add(admin1)
    session.commit()
    admin1 = (
        session.query(models.Administrator)
        .filter(models.Administrator.username == 'admin1')
        .first()
    )

    assert admin1.id is not None
    assert admin1.username == 'admin1'
    assert admin1.email == 'admin1'


def test_trainer(session):
    trainer = models.Trainer(
        username='trainer',
        email='trainer',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()
    trainer = (
        session.query(models.Trainer)
        .filter(models.Trainer.username == 'trainer')
        .first()
    )

    assert trainer.id is not None
    assert trainer.username == 'trainer'
    assert trainer.email == 'trainer'


def test_athlete(session):
    trainer = models.Trainer(
        username='trainer_athlete',
        email='trainer',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()
    trainerDb = (
        session.query(models.Trainer)
        .filter(models.Athlete.username == 'trainer_athlete')
        .first()
    )
    athlete = models.Athlete(
        username='athlete',
        email='athlete',
        unhashed_password='athlete',
        firstname='athlete',
        lastname='athlete',
        birthday=date.today(),
        gender=models.Gender.DIVERSE,
        trainer_id=trainerDb.id,
    )
    session.add(athlete)
    session.commit()
    athlete = (
        session.query(models.Athlete)
        .filter(models.Athlete.username == 'athlete')
        .first()
    )

    assert athlete.id is not None
    assert athlete.username == 'athlete'
    assert athlete.email == 'athlete'
    assert athlete.trainer == trainer
    assert trainer.athletes[0] == athlete


def test_category(session):
    category = models.Category(title='category')
    session.add(category)
    session.commit()
    category = (
        session.query(models.Category)
        .filter(models.Category.title == 'category')
        .first()
    )

    assert category.id is not None
    assert category.title == 'category'


def test_certificate(session):
    trainer = models.Trainer(
        username='trainer_athlete_certificate',
        email='trainer',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()
    trainerDb = (
        session.query(models.Trainer)
        .filter(models.Athlete.username == 'trainer_athlete_certificate')
        .first()
    )
    athlete = models.Athlete(
        username='athlete_certificate',
        email='athlete',
        unhashed_password='athlete',
        firstname='athlete',
        lastname='athlete',
        birthday=date.today(),
        gender=models.Gender.DIVERSE,
        trainer_id=trainerDb.id,
    )
    session.add(athlete)
    session.commit()
    athleteDb = (
        session.query(models.Athlete)
        .filter(models.Athlete.username == 'athlete_certificate')
        .first()
    )
    certificate = models.Certificate(
        title='certificate',
        blob=b'blob',
        athlete_id=athleteDb.id,
        uploader=trainerDb.id,
    )
    session.add(certificate)
    session.commit()
    certificate = (
        session.query(models.Certificate)
        .filter(models.Certificate.title == 'certificate')
        .first()
    )

    assert certificate.id is not None
    assert certificate.title == 'certificate'
    assert certificate.blob == b'blob'
    assert certificate.athlete == athlete
    assert certificate.uploader == trainer
    assert trainer.certificates[0] == certificate
    assert athlete.certificates[0] == certificate


def test_exercise(session):
    category = models.Category(title='category_exercise')
    session.add(category)
    session.commit()
    categoryDb = (
        session.query(models.Category)
        .filter(models.Category.title == 'category_exercise')
        .first()
    )
    exercise = models.Exercise(title='exercise', category_id=categoryDb.id)
    session.add(exercise)
    session.commit()
    exercise = (
        session.query(models.Exercise)
        .filter(models.Exercise.title == 'exercise')
        .first()
    )

    assert exercise.id is not None
    assert exercise.title == 'exercise'
    assert exercise.category == category
    assert category.exercises[0] == exercise


def test_completes(session):
    trainer = models.Trainer(
        username='trainer_athlete_completes',
        email='trainer',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.commit()
    trainerDb = (
        session.query(models.Trainer)
        .filter(models.Athlete.username == 'trainer_athlete_completes')
        .first()
    )
    athlete = models.Athlete(
        username='athlete_completes',
        email='athlete',
        unhashed_password='athlete',
        firstname='athlete',
        lastname='athlete',
        birthday=datetime.strptime('05.04.2018', '%d.%m.%Y'),
        gender=models.Gender.MALE,
        trainer_id=trainerDb.id,
    )
    session.add(athlete)
    session.commit()
    athleteDb = (
        session.query(models.Athlete)
        .filter(models.Athlete.username == 'athlete_completes')
        .first()
    )
    category = models.Category(title='category_exercise_completes')
    session.add(category)
    session.commit()
    categoryDb = (
        session.query(models.Category)
        .filter(models.Category.title == 'category_exercise_completes')
        .first()
    )
    exercise = models.Exercise(title='exercise_completes', category_id=categoryDb.id)
    session.add(exercise)
    session.commit()
    exerciseDb = (
        session.query(models.Exercise)
        .filter(models.Exercise.title == 'exercise_completes')
        .first()
    )
    completes = models.Completes(
        athlete_id=athleteDb.id,
        exercise_id=exerciseDb.id,
        tracked_at=datetime.now(),
        tracked_by=trainerDb.id,
        result='result',
        db=session,
    )
    session.add(completes)
    session.commit()
    completes = (
        session.query(models.Completes)
        .filter(models.Completes.result == 'result')
        .first()
    )

    assert completes.exercise == exercise
    assert completes.athlete == athlete
    assert completes.result == 'result'
    assert completes.trainer == trainer
    assert athlete.completes[0] == completes


def test_points_time(session):
    parse_values(session)

    # Create trainer and athlete for this test
    trainer = models.Trainer(
        username='trainer_athlete_completes',
        email='trainer',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.flush()

    athlete = models.Athlete(
        username='athlete_completes',
        email='athlete',
        unhashed_password='athlete',
        firstname='athlete',
        lastname='athlete',
        birthday=datetime.strptime('05.04.2018', '%d.%m.%Y'),
        gender=models.Gender.MALE,
        trainer_id=trainer.id,
    )
    session.add(athlete)
    session.commit()

    exerciseDb = session.scalar(
        select(models.Exercise).where(models.Exercise.title == '800 m Lauf')
    )
    completes = models.Completes(
        athlete_id=athlete.id,
        exercise_id=exerciseDb.id,
        tracked_at=athlete.birthday.replace(year=athlete.birthday.year + 6),
        tracked_by=trainer.id,
        result='00:05:16:00',
        db=session,
    )
    session.add(completes)
    exerciseDb = session.scalar(
        select(models.Exercise).where(models.Exercise.title == 'Dauer-/Geländelauf')
    )
    completes_h = models.Completes(
        athlete_id=athlete.id,
        exercise_id=exerciseDb.id,
        tracked_at=athlete.birthday.replace(year=athlete.birthday.year + 6),
        tracked_by=trainer.id,
        result='00:09:16:00',
        db=session,
    )
    session.add(completes_h)
    session.commit()

    assert completes.points == 1, f'{completes.points}'
    assert completes_h.points == 0, f'{completes.points}'


def test_points_length(session):
    parse_values(session)

    # Create trainer and athlete for this test
    trainer = models.Trainer(
        username='trainer_athlete_completes2',
        email='trainer2',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.flush()

    athlete = models.Athlete(
        username='athlete_completes2',
        email='athlete2',
        unhashed_password='athlete',
        firstname='athlete',
        lastname='athlete',
        birthday=datetime.strptime('05.04.2018', '%d.%m.%Y'),
        gender=models.Gender.MALE,
        trainer_id=trainer.id,
    )
    session.add(athlete)
    session.commit()

    exerciseDb = session.scalar(
        select(models.Exercise).where(models.Exercise.title == 'Standweitsprung')
    )
    completes = models.Completes(
        athlete_id=athlete.id,
        exercise_id=exerciseDb.id,
        tracked_at=athlete.birthday.replace(year=athlete.birthday.year + 6),
        tracked_by=trainer.id,
        result='000:001:36',
        db=session,
    )
    session.add(completes)
    session.commit()

    assert completes.points == 2, f'{completes.points}'


def test_points_times(session):
    parse_values(session)

    # Create trainer and athlete for this test
    trainer = models.Trainer(
        username='trainer_athlete_completes3',
        email='trainer3',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.flush()

    athlete = models.Athlete(
        username='athlete_completes3',
        email='athlete3',
        unhashed_password='athlete',
        firstname='athlete',
        lastname='athlete',
        birthday=datetime.strptime('05.04.2018', '%d.%m.%Y'),
        gender=models.Gender.MALE,
        trainer_id=trainer.id,
    )
    session.add(athlete)
    session.commit()

    exerciseDb = session.scalar(
        select(models.Exercise).where(models.Exercise.title == 'Drehwurf')
    )
    completes = models.Completes(
        athlete_id=athlete.id,
        exercise_id=exerciseDb.id,
        tracked_at=athlete.birthday.replace(year=athlete.birthday.year + 6),
        tracked_by=trainer.id,
        result='0025',
        db=session,
    )
    session.add(completes)
    session.commit()

    assert completes.points == 3, f'{completes.points}'


def test_points_medal(session):
    parse_values(session)

    # Create trainer and athlete for this test
    trainer = models.Trainer(
        username='trainer_athlete_completes4',
        email='trainer4',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.flush()

    athlete = models.Athlete(
        username='athlete_completes4',
        email='athlete4',
        unhashed_password='athlete',
        firstname='athlete',
        lastname='athlete',
        birthday=datetime.strptime('05.04.2018', '%d.%m.%Y'),
        gender=models.Gender.MALE,
        trainer_id=trainer.id,
    )
    session.add(athlete)
    session.commit()

    exerciseDb = session.scalar(
        select(models.Exercise).where(models.Exercise.title == 'Geräteturnen Boden')
    )
    completes = models.Completes(
        athlete_id=athlete.id,
        exercise_id=exerciseDb.id,
        tracked_at=athlete.birthday.replace(year=athlete.birthday.year + 6),
        tracked_by=trainer.id,
        result='Gold',
        db=session,
    )
    session.add(completes)
    session.commit()

    assert completes.points == 3, f'{completes.points}'
