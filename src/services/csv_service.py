import csv
from typing import Type
from fastapi import HTTPException
from sqlalchemy import inspect

from sqlalchemy.orm import Session
from src.database.database_utils import get_all

from src.models.models import Athlete, Base, Gender, Trainer

# def parse_csv(db: Session, table: Type[Base], filename: str) -> None:
#     with open


def create_csv(db: Session, table: Type[Base], filename: str) -> None:
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        result = get_all(db, table)
        if isinstance(result, HTTPException):
            raise result

        database_objects = result

        writer.writerow(get_columns(database_objects[0], True))

        for database_object in database_objects:
            writer.writerow(get_values(database_object))

def get_columns(database_object: Base, header: bool = False) -> list[str]:
    if isinstance(database_object, Trainer):
        if header:
            return ['E-Mail-Adresse', 'Vorname', 'Nachname', 'Defaultpasswort']
        return ['email', 'firstname', 'lastname', 'password']
    elif isinstance(database_object, Athlete):
        if header:
            return ['Vorname', 'Nachname', 'E-Mail', 'Geburtsdatum(TT.MM.JJJJ)', 'Geschlecht(m/w)']
        return ['firstname', 'lastname', 'email', 'birthday', 'gender']
    else:
        return [column.key for column in inspect(database_object).mapper.column_attrs]

def get_values(database_object: Base) -> list:
    values = []
    for column in get_columns(database_object, False):
        if column == 'password':
            values.append('Defaultpasswort')
        elif column == 'birthday':
            values.append(database_object.birthday.strftime('%d.%m.%Y'))
        elif column == 'gender':
            if database_object.gender == Gender.MALE:
                values.append(database_object.gender.value)
            else:
                values.append('w')
        else:
            values.append(getattr(database_object, column))

    return values
