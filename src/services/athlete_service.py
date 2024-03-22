from typing import cast
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Athlete, Base
from src.schemas.athlete_schema import AthletePatchSchema, AthletePostSchema
from src.services import update_service

def create_athlete(athlete_post_schema: AthletePostSchema, trainer_id: str, db: Session) -> Athlete:
    athlete_dict = athlete_post_schema.model_dump(exclude_unset=True)
    athlete = Athlete(**athlete_dict, trainer_id=trainer_id)
    database_utils.add(athlete, db)
    return athlete

def get_athlete_by_id(id: str, db: Session) -> Athlete:
    athlete: Base | None = database_utils.get_by_id(Athlete, id, db)

    if athlete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")

    return cast(Athlete, athlete)

def update_athlete(id: str, athlete_patch_schema: AthletePatchSchema, db: Session) -> Athlete:
    athlete: Base | None = database_utils.get_by_id(Athlete, id, db)

    if athlete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")

    update_service.update_properties(athlete, athlete_patch_schema, db)
    return cast(Athlete, athlete)

def delete_athlete(id: str, db: Session) -> None:
    return database_utils.delete(Athlete, id, db)

def get_all_athletes(db: Session) -> list[Athlete]:
    return cast(list[Athlete], database_utils.get_all(Athlete, db))
