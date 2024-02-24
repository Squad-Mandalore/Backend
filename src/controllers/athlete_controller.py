import uuid
from typing import Union, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_all, get_db, get_by_id, delete, add
from src.models.models import Athlete, Base
from src.schemas.athlete_schema import AthleteSchema, AthleteDtoSchema, AthleteUpdateSchema
from src.services.update_service import update_properties

router = APIRouter(
    # routing prefix
    prefix="/athletes",
    # documentation tag
    tags=["athletes"],
    # default response
    responses={404: {"route": "Not found"}}
)


@router.get("/all", response_model=list[AthleteSchema], status_code=status.HTTP_200_OK)
async def get_all_entries(db: Session = Depends(get_db)) -> list[Base]:
    athletes: Union[list[Base], HTTPException] = get_all(db, Athlete)
    if isinstance(athletes, HTTPException):
        raise athletes
    return athletes


@router.get("/{id}", response_model=AthleteSchema, status_code=status.HTTP_200_OK)
async def get_athlete_by_id(id: uuid.UUID, db: Session = Depends(get_db), ) -> Base:
    athlete: Union[Base, HTTPException] = get_by_id(db, Athlete, id)
    if isinstance(athlete, HTTPException):
        raise athlete
    return athlete


@router.delete("/{id}", response_model=AthleteSchema, status_code=status.HTTP_200_OK)
async def delete_by_id(id: str, db: Session = Depends(get_db)) -> None:
    athlete: Optional[HTTPException] = delete(db, Athlete, UUID(id))
    if isinstance(athlete, HTTPException):
        raise athlete
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Athlete deleted")


@router.post("/", response_model=AthleteSchema, status_code=status.HTTP_201_CREATED)
async def create_athlete(athlete_dto_schema: AthleteDtoSchema, db: Session = Depends(get_db)) -> Base:
    athlete_dto_schema.trainer_id = UUID(athlete_dto_schema.trainer_id)
    athlete_dict = athlete_dto_schema.dict(exclude_unset=True)
    athlete = Athlete(**athlete_dict)
    add(db, athlete)

    if isinstance(athlete, HTTPException):
        raise athlete
    return athlete


@router.put("/{id}", response_model=AthleteSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_athlete(id: str, athlete_update_schema: AthleteUpdateSchema, db: Session = Depends(get_db)) -> Base:
    athlete_db: Union[Base, HTTPException] = get_by_id(db, Athlete, id)
    if isinstance(athlete_db, HTTPException):
        raise athlete_db
    update_properties(athlete_db, athlete_update_schema)
    db.commit()  # Commit the changes to the database
    return athlete_db



