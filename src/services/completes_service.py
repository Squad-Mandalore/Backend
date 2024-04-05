from datetime import date
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import false, select
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from src.database import database_utils
from src.models.models import Athlete, Base, Completes, Rule
from src.schemas.completes_schema import CompletesPatchSchema, CompletesPostSchema
from src.services import update_service


def create_completes(completes_post_schema: CompletesPostSchema, db: Session) -> Completes:
    completes_dict = completes_post_schema.model_dump(exclude_unset=True)
    completes = Completes(**completes_dict)
    database_utils.add(completes, db)
    return completes

def get_completes_by_id(id: str, db: Session) -> Completes:
    completes: Base | None = database_utils.get_by_id(Completes, id, db)

    if completes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Completes not found")

    return cast(Completes, completes)

def update_completes(id: str, completes_patch_schema: CompletesPatchSchema, db: Session) -> Completes:
    completes: Base | None = database_utils.get_by_id(Completes, id, db)

    if completes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Completes not found")

    update_service.update_properties(completes, completes_patch_schema, db)
    return cast(Completes, completes)

def delete_completes(id: str, db: Session) -> None:
    return database_utils.delete(Completes, id, db)

def get_all_completes(db: Session) -> list[Completes]:
    return cast(list[Completes], database_utils.get_all(Completes, db))

def calculate_points(completes: Completes,athlete: Athlete, db: Session):
    tracket_at = completes.tracked_at
    exercise_id = completes.exercise_id
    result = completes.result
    isbigger = True
    athlete_age = tracket_at.year - athlete.birthday.year

    rule: Rule | None = db.scalar(select(Rule).where(Rule.exercise_id == exercise_id,
                                             Rule.gender == athlete.gender,
                                             Rule.from_age <= athlete_age,
                                             Rule.to_age >= athlete_age))

    if(rule == None):
        return 0

    if(rule.bronze > rule.gold):
        isbigger = False

    points = 0
    if isbigger:
        if result >= rule.gold:
            points = 3
        elif result >= rule.silver:
            points = 2
        elif result >= rule.bronze:
            points = 1
    else:
        if result <= rule.gold:
            points = 3
        elif result <= rule.silver:
            points = 2
        elif result <= rule.bronze:
            points = 1

    return points
