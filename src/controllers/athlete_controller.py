import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_all, get_db, get_by_id, delete, add
from src.models.models import Athlete, Base, Gender
from src.schemas.athlete_schema import AthleteSchema, AthleteDtoSchema
from src.services.password_service import hash_and_spice_password
from src.services.update_service import update_properties

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
    athletes:  list[Base] | HTTPException = get_all(db, Athlete)
    if isinstance(athletes, HTTPException):
        raise athletes
    return athletes


@router.get("/{id}", response_model=AthleteSchema)
async def get_athlete_by_id(id: uuid.UUID, db: Session = Depends(get_db), ) -> Base:
    athlete: Base | HTTPException = get_by_id(db, Athlete, id)
    if isinstance(athlete, HTTPException):
        raise athlete
    return athlete


@router.delete("/{id}", response_model=AthleteSchema)
async def delete_by_id(id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    athlete: HTTPException | None = delete(db, Athlete, id)
    if isinstance(athlete, HTTPException):
        raise athlete
    return athlete


@router.post("/post", response_model=AthleteSchema, status_code=status.HTTP_201_CREATED)
async def create_athlete(athlete_dto_schema: AthleteDtoSchema, db: Session = Depends(get_db)) -> Base:
    hashed_password, salt = hash_and_spice_password(athlete_dto_schema.password)    #TODO typing
    athlete = Athlete(athlete_dto_schema.username, athlete_dto_schema.email, hashed_password,
                      athlete_dto_schema.firstname, athlete_dto_schema.lastname, salt, athlete_dto_schema.birthday, UUID(athlete_dto_schema.trainer_id), athlete_dto_schema.has_disease,
                      athlete_dto_schema.gender)
    add(db, athlete)
    if isinstance(athlete, HTTPException):
        raise athlete
    return athlete


@router.put("/{id}", response_model=AthleteSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_athlete(id: str, athlete_dto_schema: AthleteDtoSchema, db: Session = Depends(get_db)) -> Base:
    athleteDb: Base | HTTPException = get_by_id(db, Athlete, id)
    if isinstance(athleteDb, HTTPException):
        raise athleteDb
    update_properties(athleteDb, athlete_dto_schema, db)
    return athleteDb



