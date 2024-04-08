from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Completes, User
from src.schemas.completes_schema import CompletesPatchSchema, CompletesPostSchema, CompletesResponseSchema
from src.services import completes_service
from src.services.auth_service import get_current_user


router = APIRouter(
    # routing prefix
    prefix="/completes",
    # documentation tag
    tags=["completes"],
    # default response
    #responses={404: {"route": "Not found"}},
)

# completes routes
@router.get("/", response_model=list[CompletesResponseSchema], status_code=status.HTTP_200_OK)
async def get_completes(
        exercise_id: str | None = Query(None),
        athlete_id: str | None = Query(None),
        tracked_at: str | None = Query(None),
        user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Completes:
    return completes_service.get_completes_by_id(exercise_id, athlete_id, tracked_at, db)

@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_ahtlete(
        exercise_id: str,
        athlete_id: str,
        tracked_at: str,
        user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    return completes_service.delete_completes(exercise_id, athlete_id, tracked_at, db)

@router.post("/", response_model=CompletesResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_completes(completes_post_schema: CompletesPostSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Completes:
    return completes_service.create_completes(completes_post_schema, user.id, db)

@router.patch("/", response_model=CompletesResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_completes(
        exercise_id: str,
        athlete_id: str,
        tracked_at: str,
        completes_patch_schema: CompletesPatchSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Completes:
    return completes_service.update_completes(exercise_id, athlete_id, tracked_at, completes_patch_schema, user.id, db)
