import csv
import random
import string
from datetime import datetime
from typing import Any, Callable, Sequence, cast

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.database_utils import add, get_all, get_db
from src.models.models import Athlete, Base, Category, Completes, Exercise, Gender, Trainer

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
        'attributes': ['athlete.lastname', 'athlete.firstname', 'athlete.gender', 'athlete.birthday_year', 'athlete.birthday', 'exercise.title', 'exercise.category.title', 'tracked_at', 'result', 'points', 'dbs']
    }
}

# Helper functions for value transformation
value_transformers: dict[str, Callable[[Any], Any]] = {
    'hashed_password': lambda _: generate_random_password(),
    'birthday': lambda d: d.strftime('%d.%m.%Y'),
    'birthday_year': lambda d: d.year,
    'gender': lambda g: g.value if g == Gender.MALE else 'w',
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

# def parse_csv(db: Session) -> None:
#     object_creator = None
#     try:
#         with open("trainer.csv0", 'r') as file:
#             reader = csv.DictReader(file)
#             header = reader.fieldnames
#             if header is None:
#                 raise ValueError("File is empty")

#             header_mapping = {
#                 tuple(entity_config['Trainer']['header']): create_trainer,
#                 tuple(entity_config['Athlete']['header']): create_athlete,
#                 tuple(entity_config['Completes']['header']): create_exercise,
#             }

#             object_creator = header_mapping.get(tuple(header))

#             if object_creator is None:
#                 raise ValueError(f"Header {header} not supported")

#             for line in reader:
#                 object = object_creator(line)
#                 if object:
#                     add(object, db)

#     except FileNotFoundError:
#         raise FileNotFoundError("File not found")
#     except Exception as e:
#         raise e

# def create_trainer(line: dict) -> Trainer:
#     return Trainer(
#         email=line['email'],
#         firstname=line['firstname'],
#         lastname=line['lastname'],
#         unhashed_password=line['password'],
#         birthday=None,
#         username=f"{line['firstname']} {line['lastname']}"
#     )

# def create_athlete(line: dict):
#     return Athlete(
#         firstname=line['firstname'],
#         lastname=line['lastname'],
#         email=line['email'],
#         birthday=datetime.strptime(line['birthday'], "%Y-%m-%dT%H:%M:%S.%f"),
#         gender=get_gender(line['gender']),
#         username=f"{line['firstname']} {line['lastname']}",
#         unhashed_password=generate_random_password(),
#         trainer_id=Depends(get_current_user)
#     )

# def create_completes(line: dict, db: Session = Depends(get_db)):
#     # 'attributes': ['athlete.lastname', 'athlete.firstname', 'athlete.gender', 'athlete.birthday_year', 'athlete.birthday', 'exercise.title', 'exercise.category.title', 'tracked_at', 'result', 'points', 'dbs']
#     athlete = db.query(Athlete).filter(Athlete.firstname == line['athlete.firstname'], Athlete.lastname == line['athlete.lastname']).first()
#     category = create_category(line)
#     exercise = create_exercise(line, category)

#     Completes(athlete_id=athlete.id, exercise_id=exercise.id, tracked_at=line['tracked_at'], completed_at=None, result=line['result'], points=line['points'], dbs=line['dbs'])

# def create_category(line: dict) -> Category:
#     # TODO: find category by title as soon as it is implemented
#     return Category(
#         title=line['exercise.category.title'],
#     )

# def create_exercise(line: dict, category: Category) -> Exercise:
#     # TODO: find exercise by title as soon as it is implemented
#     return Exercise(
#         title=line['exercise.title'],
#         category_id=category.id,
#         from_age=10,
#         to_age=20
#     )

# def get_gender(abbreviation: str) -> Gender:
#     if abbreviation == Gender.MALE.value:
#         return Gender.MALE
#     if abbreviation == Gender.FEMALE.value:
#         return Gender.FEMALE
#     if abbreviation == Gender.DIVERSE.value:
#         return Gender.DIVERSE
#     else:
#         return Gender.FEMALE


