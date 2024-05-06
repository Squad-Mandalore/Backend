import csv
import re
from datetime import date, datetime
from functools import partial
import random
import string
from typing import Any, Callable, Sequence, cast

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import extract, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_400_BAD_REQUEST

from src.database.database_utils import get_all
from src.logger.logger import logger
from src.models.models import (
    Athlete,
    Base,
    Category,
    Completes,
    Exercise,
    Gender,
    Trainer,
    User,
)

# Those header are a crime against humans in general
entity_config: dict = {
    'Trainer': {
        'header': ['E-Mail-Adresse', 'Vorname', 'Nachname', 'Defaultpasswort'],
        'filename': 'trainer.csv',
        'attributes': ['email', 'firstname', 'lastname', 'hashed_password']
    },
    'Athlete': {
        'header': ['Vorname', 'Nachname', 'E-Mail', 'Geburtsdatum', 'Geschlecht'],
        'filename': 'athlete.csv',
        'attributes': ['firstname', 'lastname', 'email', 'birthday', 'gender']
    },
    'Completes': {
        'header': ['Name', 'Vorname', 'Geschlecht', 'Geburtsjahr', 'Geburtstag', 'Übung', 'Kategorie', 'Datum', 'Ergebnis', 'Punkte', 'DBS'],
        'filename': 'completes.csv',
        'attributes': ['athlete.lastname', 'athlete.firstname', 'athlete.gender', 'athlete.birthday_year', 'athlete.birthday', 'exercise.title', 'exercise.category.title', 'tracked_at', 'result', 'points']
    }
}

def parse_input(raw_number: str, length: int, colon_index: list[int], decimals_format: str):

    number_str = raw_number.replace(',','.').replace(':','')

    number = float(number_str)
    clean_number = decimals_format.format(number)

    clean_number = clean_number.replace('.','').zfill(length)

    for pos in colon_index:
        clean_number = clean_number[:pos] + ':' + clean_number[pos:]

    return clean_number

length_parser = partial(parse_input, length=8, colon_index=[6,3], decimals_format='{:.2f}')
count_parser = partial(parse_input, length=4, colon_index=[], decimals_format='{:.0f}')
time_parser = partial(parse_input, length=9, colon_index=[6,4,2], decimals_format='{:.3f}')

parser_mapping: dict = {
    '/d/d:/d/d:/d/d:/d/d/d': time_parser,
    '/d/d/d:/d/d/d:/d/d': length_parser,
    '/d/d/d/d': count_parser,
    '/d': lambda x: x
}

def check_pattern(input:str):
    patterns = {
        r'^\d{2}:\d{2}:\d{2}:\d{3}$': '/d/d:/d/d:/d/d:/d/d/d',
        r'^\d{3}:\d{3}:\d{2}$': '/d/d/d:/d/d/d:/d/d',
        r'^\d{4}$': '/d/d/d/d',
        r'^\d$': '/d'
        }

    for pattern, output in patterns.items():
        if re.match(pattern, input):
            return output

    return 'unknown'

response_message: dict = {}

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

def create_trainer_csv(db: Session):
    trainers: Sequence[Trainer] | HTTPException = cast(Sequence[Trainer], get_all(Trainer, db))
    if isinstance(trainers, HTTPException):
        raise trainers

    write_csv(trainers, 'Trainer')

def create_athlete_csv(db: Session):
    athletes: Sequence[Athlete] | HTTPException = cast(Sequence[Athlete], get_all(Athlete, db))
    if isinstance(athletes, HTTPException):
        raise athletes

    write_csv(athletes, 'Athlete')

def create_completes_csv(db: Session):
    completes: Sequence[Completes] | HTTPException = cast(Sequence[Completes], get_all(Completes, db))
    if isinstance(completes, HTTPException):
        raise completes

    write_csv(completes, 'Completes')

def write_csv(entities: Sequence[Base], entity_type: str) -> None:
    if not entities:
        return

    config: dict = entity_config[entity_type]
    filename: str = config['filename']
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
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
    response_message.clear()
    object_creator = None
    file_content = await file.read()
    content_str = file_content.decode("utf-8")
    lines = content_str.splitlines()
    reader = csv.DictReader(lines, delimiter=';')
    header = reader.fieldnames

    if header is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    if header[0] == "Externe ID":
        header = header[1:]

    header_mapping = {
        tuple(entity_config['Trainer']['header']): lambda line: create_trainer(line, db),
        tuple(entity_config['Athlete']['header']): lambda line: create_athlete(line, current_user, db),
        tuple(entity_config['Completes']['header']): lambda line: create_completes(line, current_user, db),
    }

    object_creator = header_mapping.get(tuple(header))

    if object_creator is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Header {header} not supported")

    transaction = db.begin_nested()
    try:
        for line in reader:
            object = object_creator(line)
            if object:
                db.add(object)

        transaction.commit()
    except HTTPException as e:
        transaction.rollback()
        raise e
    except Exception as e:
        transaction.rollback()
        logger.error(f"Error while parsing csv: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error while parsing csv")

    return response_message

def create_trainer(line: dict, db: Session) -> Trainer:
    # check if values are not empty
    if not line['E-Mail-Adresse'] or not line['Vorname'] or not line['Nachname'] or not line['Defaultpasswort']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Values are missing")

    # check if the email with first and lastname is already taken
    if db.scalar(select(Trainer).where(Trainer.email == line['E-Mail-Adresse'])):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Trainer with email {line['E-Mail-Adresse']} already exists")

    return Trainer(
        email=line['E-Mail-Adresse'],
        firstname=line['Vorname'],
        lastname=line['Nachname'],
        unhashed_password=line['Defaultpasswort'],
        username=f"{line['Vorname']} {line['Nachname']} {line['E-Mail-Adresse']}",
    )

def create_athlete(line: dict, current_user: User, db: Session) -> Athlete | None:
    # check if values are not empty
    if not line['Vorname'] or not line['Nachname'] or not line['E-Mail'] or not line['Geburtsdatum']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Values are missing")

    try:
        birthday = datetime.strptime(line['Geburtsdatum'], "%d.%m.%Y").date()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Birthday is not in the right format")

    # check if the email with birthday is already taken
    if db.scalar(select(Athlete).where(Athlete.email == line['E-Mail'], Athlete.birthday == birthday)):
        global response_message
        # add error message to response_message
        response_message[f"{line['Vorname']} {line['Nachname']} {line['E-Mail']}"] = "Athlete already exists"
        return None

    return Athlete(
        firstname=line['Vorname'],
        lastname=line['Nachname'],
        email=line['E-Mail'],
        birthday=birthday,
        gender=get_gender(line['Geschlecht']),
        username=f"{line['Vorname']} {line['Nachname']} {line['E-Mail']}",
        unhashed_password=generate_random_password(),
        trainer_id=current_user.id
    )

def create_completes(line: dict, current_user: User, db: Session) -> Completes | None:
    # 'attributes': ['athlete.lastname', 'athlete.firstname', 'athlete.gender', 'athlete.birthday_year', 'athlete.birthday', 'exercise.title', 'exercise.category.title', 'tracked_at', 'result', 'points', 'dbs']
    # 'header': ['Name', 'Vorname', 'Geschlecht', 'Geburtsjahr', 'Geburtstag', 'Übung', 'Kategorie', 'Datum', 'Ergebnis', 'Punkte', 'DBS'],
    # check if values are not empty
    if not line['Name'] or not line['Vorname'] or not line['Geschlecht'] or not line['Übung'] or not line['Kategorie'] or not line['Datum'] or not line['Ergebnis'] or not line['Punkte']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Values are missing")

    try:
        tracked_at = datetime.strptime(line['Datum'], "%d.%m.%Y").date()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date is not in the right format")

    if not line['Geburtstag']:
        if not line['Geburtsjahr']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Birthday is missing")
        birthday = datetime.strptime(f"01.01.{line['Geburtsjahr']}", "%d.%m.%Y").date()
        athlete = db.scalar(select(Athlete).where(Athlete.firstname == line['Vorname'], Athlete.lastname == line['Name'], extract('year', Athlete.birthday) == birthday.year))
    else:
        birthday = datetime.strptime(line['Geburtstag'], "%d.%m.%Y").date()
        athlete = db.scalar(select(Athlete).where(Athlete.firstname == line['Vorname'], Athlete.lastname == line['Name'], Athlete.birthday == birthday))

    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Athlete {line['Vorname']} {line['Name']} {birthday} not found")

    global response_message
    category = create_category(line, db)
    exercise = db.scalar(select(Exercise).where(Exercise.title == line['Übung']))
    #exercise = create_exercise(line, category, db)
    if exercise == None:
        response_message[f"{line['Übung']}"] = 'Skipped completes for this exercise'
        return

    value: str = line['Ergebnis']
    if exercise.rules == None or len(exercise.rules) <= 0:
        response_message[f"{exercise.title}"] = 'No Rules found for this exercise'
        return

    pattern = check_pattern(exercise.rules[0].gold)
    value = parser_mapping[pattern](line['Ergebnis'])

    # check if completes already exists
    completes = db.scalar(select(Completes).where(Completes.athlete_id == athlete.id, Completes.exercise_id == exercise.id, Completes.tracked_at == tracked_at))
    if not completes:
        return Completes(
            athlete_id=athlete.id,
            exercise_id=exercise.id,
            tracked_at=tracked_at,
            result=value,
            tracked_by=current_user.id,
            db=db
        )
    else:
        if int(line['Punkte']) > int(completes.points):
            #global response_message
            response_message[f"{line['Vorname']} {line['Name']} {line['Datum']} {line['Übung']}"] = f"Points updated from {completes.points} to {line['Punkte']}"
            completes.result = value
            completes.points = line['Punkte']
            db.flush()

def create_category(line: dict, db: Session) -> Category:
    category = db.scalar(select(Category).where(Category.title == line['Kategorie']))
    if not category:
        category = Category(
            title=line['Kategorie'],
        )
        db.add(category)
        db.flush()
        return category

    return category

def create_exercise(line: dict, category: Category, db: Session) -> Exercise:
    exercise = db.scalar(select(Exercise).where(Exercise.title == line['Übung']))
    if not exercise:
        exercise = Exercise(
            title=line['Übung'],
            category_id=category.id,
        )
        db.add(exercise)
        db.flush()
        return exercise

    return exercise

def get_gender(abbreviation: str) -> Gender:
    abbreviation = abbreviation.lower()
    if abbreviation == Gender.MALE.value:
        return Gender.MALE
    if abbreviation == Gender.FEMALE.value:
        return Gender.FEMALE
    if abbreviation == Gender.DIVERSE.value:
        return Gender.DIVERSE
    else:
        return Gender.FEMALE
