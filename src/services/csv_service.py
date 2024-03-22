import csv
import random
import string
from datetime import date, datetime
from typing import Any, Callable, Sequence, cast

from fastapi import Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from src.database.database_utils import add, get_all, get_db
from src.models.models import Athlete, Base, Category, Completes, Exercise, Gender, Trainer, User
from src.services.auth_service import get_current_user
from src.logger.logger import logger

# Those header are a crime against humans in general
entity_config: dict = {
    'Trainer': {
        'header': ['E-Mail-Adresse', 'Vorname', 'Nachname', 'Defaultpasswort'],
        'filename': 'trainer.csv',
        'attributes': ['email', 'firstname', 'lastname', 'hashed_password']
    },
    'Athlete': {
        'header': ['Vorname', 'Nachname', 'E-Mail', 'Geburtsdatum(TT.MM.JJJJ)', 'Geschlecht(m/w)'],
        'filename': 'athlete.csv',
        'attributes': ['firstname', 'lastname', 'email', 'birthday', 'gender']
    },
    'Completes': {
        'header': ['Name', 'Vorname', 'Geschlecht', 'Geburtsjahr', 'Geburtstag', 'Übung', 'Kategorie', 'Datum', 'Ergebnis', 'Punkte', 'DBS'],
        'filename': 'completes.csv',
        'attributes': ['athlete.lastname', 'athlete.firstname', 'athlete.gender', 'athlete.birthday_year', 'athlete.birthday', 'exercise.title', 'exercise.category.title', 'tracked_at', 'result', 'points']
    }
}

# Helper functions for value transformation
value_transformers: dict[str, Callable[[Any], Any]] = {
    'hashed_password': lambda _: generate_random_password(),
    'birthday': lambda d: d.strftime('%d.%m.%Y'),
    'birthday_year': lambda d: d.year,
    'gender': lambda g: g.value if g == Gender.MALE else 'w',
    'tracked_at': lambda d: d.strftime('%d.%m.%Y'),
}

def create_csv(db: Session) -> None:
    trainers: Sequence[Trainer] | HTTPException = cast(Sequence[Trainer], get_all(Trainer, db))
    if isinstance(trainers, HTTPException):
        raise trainers

    athletes: Sequence[Athlete] | HTTPException = cast(Sequence[Athlete], get_all(Athlete, db))
    if isinstance(athletes, HTTPException):
        raise athletes

    completes: Sequence[Completes] | HTTPException = cast(Sequence[Completes], get_all(Completes, db))
    if isinstance(completes, HTTPException):
        raise completes

    write_csv(trainers, 'Trainer')
    write_csv(athletes, 'Athlete')
    write_csv(completes, 'Completes')

def write_csv(entities: Sequence[Base], entity_type: str) -> None:
    if not entities:
        return

    config: dict = entity_config[entity_type]
    filename: str = config['filename']
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(config['header'])

        for enitity in entities:
            writer.writerow(get_values(enitity, config))


def get_values(entity: Base, config: dict) -> list:
    values: list = []
    for attribute in config['attributes']:
        if attribute in value_transformers:
            value = value_transformers[attribute](getattr(entity, attribute.split('.')[0]))
        elif '.' in attribute:
            attribute_parts = attribute.split('.')
            entity_temp = entity
            for part in attribute_parts:
                if part in value_transformers:
                    if part == 'birthday_year':
                        entity_temp = value_transformers[part](getattr(entity_temp, 'birthday'))
                        continue
                    entity_temp = value_transformers[part](getattr(entity_temp, part))
                    continue
                entity_temp = getattr(entity_temp, part)
            value = entity_temp
        else:
            value = getattr(entity, attribute)
        values.append(value)
    return values

def generate_random_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

async def parse_csv(file: UploadFile, current_user: User, db: Session) -> dict | None:
    object_creator = None
    file_content = await file.read()
    content_str = file_content.decode("utf-8")
    lines = content_str.splitlines()
    reader = csv.DictReader(lines)
    header = reader.fieldnames

    if header is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    header_mapping = {
        tuple(entity_config['Trainer']['header']): lambda line: create_trainer(line, db),
        tuple(entity_config['Athlete']['header']): lambda line: create_athlete(line, current_user, db),
        tuple(entity_config['Completes']['header']): lambda line: create_completes(line, db),
    }

    object_creator = header_mapping.get(tuple(header))

    if object_creator is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Header {header} not supported")

    transaction = db.begin_nested()
    user_flag = False
    try:
        for line in reader:
            object = object_creator(line)
            if object:
                db.add(object)
            else:
                if header == entity_config['Athlete']['header']:
                    user_flag = True

        transaction.commit()
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        transaction.rollback()
        logger.error(f"Error while parsing csv: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error while parsing csv")


    if user_flag:
        return {"detail": "Users were skipped"}

def create_trainer(line: dict, db: Session) -> Trainer:
    # check if the email with first and lastname is already taken
    if db.query(Trainer).filter(Trainer.email == line['E-Mail-Adresse']).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Trainer with email {line['E-Mail-Adresse']} already exists")

    return Trainer(
        email=line['E-Mail-Adresse'],
        firstname=line['Vorname'],
        lastname=line['Nachname'],
        unhashed_password=line['Defaultpasswort'],
        birthday=None,
        username=f"{line['Vorname']} {line['Nachname']} {line['E-Mail-Adresse']}",
    )

def create_athlete(line: dict, current_user: User, db: Session) -> Athlete | None:
    # check if the email with birthday is already taken
    if db.query(Athlete).filter(Athlete.email == line['E-Mail'], Athlete.birthday == datetime.strptime(line['Geburtsdatum(TT.MM.JJJJ)'], "%d.%m.%Y")).first():
        return None

    return Athlete(
        firstname=line['Vorname'],
        lastname=line['Nachname'],
        email=line['E-Mail'],
        birthday=datetime.strptime(line['Geburtsdatum(TT.MM.JJJJ)'], "%d.%m.%Y").date(),
        gender=get_gender(line['Geschlecht(m/w)']),
        username=f"{line['Vorname']} {line['Nachname']} {line['E-Mail']}",
        unhashed_password=generate_random_password(),
        trainer_id=current_user.id
    )

def create_completes(line: dict, db: Session) -> Completes:
    # 'attributes': ['athlete.lastname', 'athlete.firstname', 'athlete.gender', 'athlete.birthday_year', 'athlete.birthday', 'exercise.title', 'exercise.category.title', 'tracked_at', 'result', 'points', 'dbs']
    # 'header': ['Name', 'Vorname', 'Geschlecht', 'Geburtsjahr', 'Geburtstag', 'Übung', 'Kategorie', 'Datum', 'Ergebnis', 'Punkte', 'DBS'],
    athlete = db.query(Athlete).filter(Athlete.firstname == line['Vorname'], Athlete.lastname == line['Name'], Athlete.birthday == datetime.strptime(line['Geburtstag'], "%d.%m.%Y").date()).first()
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Athlete {line['Vorname']} {line['Name']} {line['Geburtstag']} not found")

    category = create_category(line, db)
    exercise = create_exercise(line, category, db)

    return Completes(
        athlete_id=athlete.id,
        exercise_id=exercise.id,
        tracked_at=datetime.strptime(line['Datum'], "%d.%m.%Y").date(),
        completed_at=None,
        result=line['Ergebnis'],
        points=line['Punkte'],
        dbs=line['DBS'].lower() == 'true'
    )

def create_category(line: dict, db: Session) -> Category:
    category = db.query(Category).filter(Category.title == line['Kategorie']).first()
    if not category:
        category = Category(
            title=line['Kategorie'],
        )
        db.add(category)
        db.flush()
        return category

    return category

def create_exercise(line: dict, category: Category, db: Session) -> Exercise:
    exercise = db.query(Exercise).filter(Exercise.title == line['Übung']).first()
    if not exercise:
        exercise = Exercise(
            title=line['Übung'],
            category_id=category.id,
            from_age=10,
            to_age=20
        )
        db.add(exercise)
        db.flush()
        return exercise

    return exercise


def get_gender(abbreviation: str) -> Gender:
    if abbreviation == Gender.MALE.value:
        return Gender.MALE
    if abbreviation == Gender.FEMALE.value:
        return Gender.FEMALE
    if abbreviation == Gender.DIVERSE.value:
        return Gender.DIVERSE
    else:
        return Gender.FEMALE


