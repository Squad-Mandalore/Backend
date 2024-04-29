from datetime import datetime
from typing import cast
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from src.database import database_utils
from src.models.models import Athlete, Base, User
from src.schemas.athlete_schema import AthletePatchSchema, AthletePostSchema
from src.services import update_service

def create_athlete(athlete_post_schema: AthletePostSchema, trainer_id: str, db: Session) -> Athlete:
    user_db: User | None = db.scalar(select(User).where(User.username == athlete_post_schema.username))
    if user_db is not None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Username already in use")

    athlete_dict = athlete_post_schema.model_dump(exclude_unset=True)
    athlete = Athlete(**athlete_dict, trainer_id=trainer_id)
    database_utils.add(athlete, db)
    return athlete

def get_athlete_by_id(id: str, db: Session) -> Athlete:
    athlete: Base | None = db.get(Athlete, id)

    if athlete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")

    return cast(Athlete, athlete)

def update_athlete(id: str, athlete_patch_schema: AthletePatchSchema, db: Session) -> Athlete:
    athlete: Athlete = get_athlete_by_id(id, db)
    if athlete_patch_schema.username != None and athlete.username != athlete_patch_schema.username:
        user_db: User | None = db.scalar(select(User).where(User.username == athlete_patch_schema.username))
        if user_db is not None:
            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Username already in use")

    if athlete_patch_schema.unhashed_password != None:
        update_service.update_password(athlete, athlete_patch_schema.unhashed_password)
        athlete_patch_schema.unhashed_password = None

    update_service.update_properties(athlete, athlete_patch_schema)
    setattr(athlete, "last_edited_at", datetime.now())
    db.commit()
    return cast(Athlete, athlete)

def delete_athlete(id: str, db: Session) -> None:
    return database_utils.delete(Athlete, id, db)

def get_all_athletes(db: Session) -> list[Athlete]:
    return cast(list[Athlete], database_utils.get_all(Athlete, db))
