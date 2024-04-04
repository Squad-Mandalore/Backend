from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Exercise, User
from src.schemas.exercise_schema import ExercisePatchSchema, ExercisePostSchema, ExerciseResponseSchema
from src.services import exercise_service
from src.services.auth_service import get_current_user


router = APIRouter(
    # routing prefix
    prefix="/exercises",
    # documentation tag
    tags=["exercises"],
    # default response
    #responses={404: {"route": "Not found"}},
)

# exercise routes
@router.get("/all", response_model=list[ExerciseResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_exercises(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Exercise]:
    return exercise_service.get_all_exercises(db)

@router.get("/{id}", response_model=ExerciseResponseSchema, status_code=status.HTTP_200_OK)
async def get_exercise(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Exercise:
    return exercise_service.get_exercise_by_id(id, db)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_ahtlete(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    return exercise_service.delete_exercise(id, db)

@router.post("/", response_model=ExerciseResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_exercise(exercise_post_schema: ExercisePostSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Exercise:
    return exercise_service.create_exercise(exercise_post_schema, db)

@router.patch("/{id}", response_model=ExerciseResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_exercise(id: str, exercise_patch_schema: ExercisePatchSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Exercise:
    return exercise_service.update_exercise(id, exercise_patch_schema, db)
