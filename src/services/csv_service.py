import csv
from datetime import datetime
from typing import Sequence, cast

from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from src.database.database_utils import add, get_all
from src.models.models import Athlete, Base, Completes, Gender, Trainer


# Those header are a crime against humans in general
trainer_header: list[str] = ['E-Mail-Adresse', 'Vorname', 'Nachname', 'Defaultpasswort']
trainer_filename: str = "trainer.csv"
athlete_header: list[str] = ['Vorname', 'Nachname', 'E-Mail', 'Geburtsdatum(TT.MM.JJJJ)', 'Geschlecht(m/w)']
athlete_filename: str = "athlete.csv"
exercise_header: list[str] = ['Name', 'Vorname', 'Geschlecht', 'Geburtsjahr', 'Geburtstag', 'Übung', 'Kategorie', 'Datum', 'Ergebnis', 'Punkte', 'DBS']
exercise_filename: str = "exercise.csv"

def create_csv(db: Session) -> None:
    result: Sequence[Trainer] | HTTPException = cast(Sequence[Trainer], get_all(Trainer, db))
    if isinstance(result, HTTPException):
        raise result

    for trainer_count, trainer in enumerate(result):
        write_csv(result, trainer_header, trainer_filename + str(trainer_count))
        write_csv(trainer.athletes, athlete_header, athlete_filename + str(trainer_count))
        for athlete_count, athlete in enumerate(trainer.athletes):
            write_csv(athlete.completes, exercise_header, exercise_filename + str(trainer_count) + str(athlete_count))

def write_csv(database_objects: Sequence[Base], header: list[str], filename: str) -> None:
    if not database_objects:
        return

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for database_object in database_objects:
            writer.writerow(get_values(database_object))


def get_columns(database_object: Base) -> list[str]:
    if isinstance(database_object, Trainer):
        return ['email', 'firstname', 'lastname', 'password']
    elif isinstance(database_object, Athlete):
        return ['firstname', 'lastname', 'email', 'birthday', 'gender']
    elif isinstance(database_object, Completes):
        return ['lastname', 'firstname', 'gender', 'birthday_year', 'birthday', 'exercise.title', 'exercise.category.title', 'tracked_at', 'result', 'points', 'dbs']
    else:
        return [column.key for column in inspect(database_object).mapper.column_attrs]

def get_values(database_object: Base) -> list:
    values = []
    for column in get_columns(database_object):
        if column == 'password':
            values.append('Defaultpasswort')
        elif column == 'birthday':
            values.append(database_object.birthday.strftime('%d.%m.%Y'))
        elif column == 'gender':
            if database_object.gender == Gender.MALE:
                values.append(database_object.gender.value)
            else:
                values.append('w')
        elif column == 'exercise.title':
            values.append(database_object.exercise.title)
        elif column == 'exercise.category.title':
            values.append(database_object.exercise.category.title)
        else:
            values.append(getattr(database_object, column))

    return values

def parse_csv(db: Session) -> None:
    with open("trainer.csv0", 'r') as file:
        reader = csv.reader(file.readlines())

        # todo: find out how to trigger __next__ builtin function
        for line in reader:
            if line == trainer_header:
                trainer = True
                break
            if line == athlete_header:
                athlete = True
                break
            if line == exercise_header:
                exercise = True
                break

        # maybe for this step a reference to the existing controllers so there is not that much boiler plate code
        for line in reader:
            if trainer:
                # ['email', 'firstname', 'lastname', 'password']
                # todo: ask about what is the username used for and whats the value
                add(Trainer(email=line[0], firstname=line[1], lastname=line[2], unhashed_password=line[3],
                               birthday=None, username="Meowzer"), db)
            elif athlete:
                # ['firstname', 'lastname', 'email', 'birthday', 'gender']
                # todo: ask about where to get the associated trainer from
                add(Athlete(firstname=line[0], lastname=line[1], email=line[2], birthday=datetime.strptime(line[3], "%Y-%m-%dT%H:%M:%S.%f"), gender=get_gender(line[4]),
                            username="Woofzer", unhashed_password="YourMoma", trainer_id="big question"), db)
            elif exercise:
                # ['lastname', 'firstname', 'gender', 'birthday_year', 'birthday', 'exercise.title', 'exercise.category.title', 'tracked_at', 'result', 'points', 'dbs']
                # even more handling needs to be done for the athletes respectively


def get_gender(abbreviation: str) -> Gender:
    if abbreviation == Gender.MALE.value:
        return Gender.MALE
    if abbreviation == Gender.FEMALE.value:
        return Gender.FEMALE
    if abbreviation == Gender.DIVERSE.value:
        return Gender.DIVERSE
    else:
        return Gender.FEMALE

