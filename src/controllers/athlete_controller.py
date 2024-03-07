from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.database_utils import add, delete, get_all, get_by_id, get_db
from src.models.models import Athlete, Base
from src.schemas.athlete_schema import (
    AthletePatchSchema,
    AthletePostSchema,
    AthleteResponseSchema,
)
from src.services.auth_service import get_current_user
from src.services.update_service import update_properties

router = APIRouter(
    # routing prefix
    prefix="/athletes",
    # documentation tag
    tags=["athletes"],
    # default response
    responses={404: {"route": "Not found"}},
)

@router.get("/all", response_model=list[AthleteResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_entries(user: get_current_user = Depends(), db: Session = Depends(get_db)) -> list[Base]:
    if isinstance(user, HTTPException):
        raise user
    return get_all(Athlete, db)

@router.get("/{id}", response_model=AthleteResponseSchema, status_code=status.HTTP_200_OK)
async def get_athlete_by_id(id: str, user: get_current_user = Depends(), db: Session = Depends(get_db), ) -> Base:
    if isinstance(user, HTTPException):
        raise user
    
    athlete: Base | None = get_by_id(Athlete, id, db)

    if athlete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")
    return athlete


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_by_id(id: str, user: get_current_user = Depends(), db: Session = Depends(get_db)) -> None:
    if isinstance(user, HTTPException):
        raise user
    
    return delete(Athlete, id, db)

@router.post("/", response_model=AthleteResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_athlete(athlete_post_schema: AthletePostSchema, user: get_current_user = Depends(), db: Session = Depends(get_db)) -> Base:
    if isinstance(user, HTTPException):
        raise user
    
    athlete_dict = athlete_post_schema.model_dump(exclude_unset=True)
    athlete = Athlete(**athlete_dict)
    add(athlete, db)

    if isinstance(athlete, HTTPException):
        raise athlete
    return athlete


@router.patch("/{id}", response_model=AthleteResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_athlete(id: str, athlete_patch_schema: AthletePatchSchema, user: get_current_user = Depends(), db: Session = Depends(get_db)) -> Base:
    if isinstance(user, HTTPException):
        raise user
    
    athlete: Base | None = get_by_id(Athlete, id, db)

    if athlete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")
    update_properties(athlete, athlete_patch_schema, db)
    return athlete



