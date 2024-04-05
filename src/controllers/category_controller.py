from typing import Union
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Category, Exercise, User
from src.schemas.category_schema import CategoryExerciseFullResponseSchema, CategoryFullResponseSchema
from src.services import category_service
from src.services.auth_service import get_current_user


router = APIRouter(
    # routing prefix
    prefix="/categories",
    # documentation tag
    tags=["categories"],
    # default response
    #responses={404: {"route": "Not found"}},
)

@router.get("/", response_model=Union[list[CategoryExerciseFullResponseSchema], list[CategoryFullResponseSchema]], status_code=status.HTTP_200_OK)
async def get_categories_by_id(
        category_id: str | None = Query(None),
        athlete_id: str | None = Query(None),
        user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Category] | list[Exercise]:
    # check if return value is a list of categories or a list of exercises
    return category_service.get_category_by_id(category_id, athlete_id, db)
