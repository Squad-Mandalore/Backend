import csv
from typing import Type
from fastapi import HTTPException
from sqlalchemy import inspect

from sqlalchemy.orm import Session
from src.database.database_utils import get_all

from src.models.models import Base

# function to create a csv file from a list of database objects
def create_csv(db: Session, table: Type[Base], filename: str) -> None:
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        result = get_all(db, table)
        if isinstance(result, HTTPException):
            raise result

        database_objects = result

        writer.writerow(get_columns(database_objects[0]))

        for database_object in database_objects:
            writer.writerow([getattr(database_object, column) for column in get_columns(database_object)])

def get_columns(columns: Base) -> list:
    return [column.key for column in inspect(columns).mapper.column_attrs]
