from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_all, get_db, get_by_id, delete
from src.models.models import Athlete, Base
from src.schemas.athlete_schema import AthleteSchema

router = APIRouter(
    # routing prefix
    prefix="/athletes",
    # documentation tag
    tags=["athletes"],
    # default response
    responses={404: {"route": "Not found"}}
)


@router.get("/all", response_model=list[AthleteSchema])
async def get_all_entries(db: Session = Depends(get_db)) -> list[Base]:
    athletes = get_all(db, Athlete)
    if isinstance(athletes, HTTPException):
        raise athletes
    return athletes


@router.get("/{id}", response_model=AthleteSchema)
async def get_athlete_by_id(id: str, db: Session = Depends(get_db), ) -> Base:
    athlete = get_by_id(db, Athlete, id)
    if isinstance(athlete, HTTPException):
        raise athlete
    return athlete


@router.delete("/{id}", response_model=AthleteSchema)
async def delete_by_id(id: str, db: Session = Depends(get_db) ) -> None:
    athlete = delete(db, Athlete, id)
    if isinstance(athlete, HTTPException):
        raise athlete
    return athlete

@router.post("", response_model=AthleteSchema, status_code=status.HTTP_201_CREATED)
async def create_athlete(db: Session = Depends(get_db())) -> Base:
    Athlete()