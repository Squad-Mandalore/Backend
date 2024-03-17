from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Athlete, Base, User
from src.schemas.athlete_schema import (
    AthletePatchSchema,
    AthletePostSchema,
    AthleteResponseSchema,
)
from src.services import athlete_service
from src.services.auth_service import get_current_user

router = APIRouter(
    # routing prefix
    prefix="/athletes",
    # documentation tag
    tags=["athletes"],
    # default response
    #responses={404: {"route": "Not found"}},
)

@router.get("/all", response_model=list[AthleteResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_athletes(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Athlete]:
    return athlete_service.get_all_athletes(db)

@router.get("/{id}", response_model=AthleteResponseSchema, status_code=status.HTTP_200_OK)
async def get_athlete(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Athlete:
    return athlete_service.get_athlete_by_id(id, db)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_ahtlete(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    return athlete_service.delete_athlete(id, db)

@router.post("/", response_model=AthleteResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_athlete(athlete_post_schema: AthletePostSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Athlete:
    return athlete_service.create_athlete(athlete_post_schema, db)

@router.patch("/{id}", response_model=AthleteResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_athlete(id: str, athlete_patch_schema: AthletePatchSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Base:
    return athlete_service.update_athlete(id, athlete_patch_schema, db)

