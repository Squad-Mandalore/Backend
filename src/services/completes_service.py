from datetime import datetime
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import false, select
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from src.database import database_utils
from src.models.models import Athlete, Base, Completes, Rule
from src.schemas.completes_schema import CompletesPatchSchema, CompletesPostSchema
from src.services import update_service
from src.logger.logger import logger


def create_completes(completes_post_schema: CompletesPostSchema, current_user_id: str, db: Session) -> Completes:
    completes_dict = completes_post_schema.model_dump(exclude_unset=True)
    completes = Completes(**completes_dict, tracked_by=current_user_id, tracked_at=datetime.now().date())
    database_utils.add(completes, db)
    return completes

def get_completes_by_id(exercise_id: str | None, athlete_id: str | None, tracked_at: str | None, db: Session) -> Completes:
    query = db.query(Completes)

    if athlete_id is not None:
        query = query.filter(Completes.athlete_id == athlete_id)
    if exercise_id is not None:
        query = query.filter(Completes.exercise_id == exercise_id)
    if tracked_at is not None:
        date = datetime.strptime(tracked_at, "%Y-%m-%d").date()
        query = query.filter(Completes.tracked_at == date)

    completes = query.all()

    if completes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Completes not found")

    return cast(Completes, completes)

def update_completes(exercise_id: str, athlete_id: str, tracked_at: str, completes_patch_schema: CompletesPatchSchema, current_user_id: str, db: Session) -> Completes:
    # Convert the tracked_at string to a datetime object
    date = datetime.strptime(tracked_at, "%Y-%m-%d").date()

    # Locate the specific entry to delete
    completes = db.get(Completes, (athlete_id, exercise_id, date))

    # If no such entry exists, raise a 404 error
    if not completes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Completes not found")

    update_service.update_properties(completes, completes_patch_schema)
    setattr(completes, "tracked_at", datetime.now().date())
    setattr(completes, "tracked_by", current_user_id)
    db.commit()
    return cast(Completes, completes)

def delete_completes(exercise_id: str, athlete_id: str, tracked_at: str, db: Session) -> None:
    # Convert the tracked_at string to a datetime object
    date = datetime.strptime(tracked_at, "%Y-%m-%d").date()

    # Locate the specific entry to delete
    completes = db.get(Completes, (athlete_id, exercise_id, date))

    # Delete the entry
    db.delete(completes)
    db.commit()

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
