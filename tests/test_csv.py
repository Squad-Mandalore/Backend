from datetime import date, datetime

from src.models.models import (
    Athlete,
    Category,
    Completes,
    Exercise,
    Gender,
    Trainer,
)
from src.services.csv_service import (
    check_pattern,
    count_parser,
    length_parser,
    parser_mapping,
    time_parser,
)
from tests.define_test_variables import TestVariables


def create_athletes(session):
    trainer = Trainer(
        username='trainer_athlete_completes',
        email='trainer',
        unhashed_password='trainer',
        firstname='trainer',
        lastname='trainer',
    )
    session.add(trainer)
    session.flush()
    athlete = Athlete(
        username='athlete_completes',
        email='athlete',
        unhashed_password='athlete',
        firstname='athlete',
        lastname='athlete',
        birthday=date.today(),
        gender=Gender.DIVERSE,
        trainer_id=trainer.id,
    )
    session.add(athlete)
    session.flush()
    category = Category(title='category_exercise_completes')
    session.add(category)
    session.flush()
    exercise = Exercise(title='exercise_completes', category_id=category.id)
    session.add(exercise)
    session.flush()
    completes = Completes(
        athlete_id=athlete.id,
        exercise_id=exercise.id,
        tracked_at=datetime.now(),
        tracked_by=trainer.id,
        result='result',
        db=session,
    )
    session.add(completes)
    session.commit()


def test_csv(session, client):
    create_athletes(session)
    response = client.get(TestVariables.BASEURL + '/csv/trainer.csv')
    assert response.status_code == 200, f'{response.text} {response.status_code}'
    response = client.get(TestVariables.BASEURL + '/csv/athlete.csv')
    assert response.status_code == 200, f'{response.text} {response.status_code}'
    response = client.get(TestVariables.BASEURL + '/csv/completes.csv')
    assert response.status_code == 200, f'{response.text} {response.status_code}'

    response = client.post(
        TestVariables.BASEURL + '/csv/parse',
        files={'file': ('trainer.csv', open('trainer.csv', 'rb'))},
        headers=TestVariables.headers,
    )
    assert response.status_code == 400, f'{response.text} {response.status_code}'
    response = client.post(
        TestVariables.BASEURL + '/csv/parse',
        files={'file': ('real_athletes.csv', open('./tests/real_athletes.csv', 'rb'))},
        headers=TestVariables.headers,
    )
    assert response.status_code == 201, f'{response.text} {response.status_code}'
    response = client.post(
        TestVariables.BASEURL + '/csv/parse',
        files={
            'file': ('real_completes.csv', open('./tests/real_completes.csv', 'rb'))
        },
        headers=TestVariables.headers,
    )
    assert response.status_code == 201, f'{response.text} {response.status_code}'
    response = client.post(
        TestVariables.BASEURL + '/csv/parse',
        files={
            'file': (
                'real_completes_untrimmed.csv',
                open('./tests/real_completes_untrimmed.csv', 'rb'),
            )
        },
        headers=TestVariables.headers,
    )
    assert response.status_code == 201, f'{response.text} {response.status_code}'


def test_length_parser():
    assert length_parser(raw_number='15,3') == '000:015:30'
    assert length_parser(raw_number='29') == '000:029:00'
    assert length_parser(raw_number='16,35') == '000:016:35'


def test_count_parser():
    assert count_parser(raw_number='14') == '0014'
    assert count_parser(raw_number='3') == '0003'


def test_time_parser():
    assert time_parser(raw_number='14,34') == '00:00:14:340'
    assert time_parser(raw_number='3') == '00:00:03:000'
    assert time_parser(raw_number='14:00') == '00:14:00:000'
    assert time_parser(raw_number='03:45') == '00:03:45:000'


def test_check_pattern():
    pattern = check_pattern('your mom')
    value = parser_mapping[pattern]('14,34')
    assert value is None
