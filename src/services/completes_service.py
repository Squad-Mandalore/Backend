from datetime import datetime
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Base, Completes
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
    completes = db.query(Completes).filter(
        Completes.exercise_id == exercise_id,
        Completes.athlete_id == athlete_id,
        Completes.tracked_at == date
    ).first()

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
    completes = db.query(Completes).filter(
        Completes.exercise_id == exercise_id,
        Completes.athlete_id == athlete_id,
        Completes.tracked_at == date
    ).first()

    # If no such entry exists, raise a 404 error
    if not completes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Completes not found")

    # Delete the entry
    db.delete(completes)
    db.commit()
