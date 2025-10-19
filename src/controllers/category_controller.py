from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Category, User
from src.schemas.category_schema import (
    CategoryFullResponseSchema,
    CategoryVeryFullResponseSchema,
)
from src.services import category_service
from src.services.auth_service import get_current_user

router = APIRouter(
    # routing prefix
    prefix='/categories',
    # documentation tag
    tags=['categories'],
    # default response
    # responses={404: {"route": "Not found"}},
)


@router.get(
    '/',
    response_model=list[CategoryVeryFullResponseSchema]
    | list[CategoryFullResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_categories_by_athlete_id(
    athlete_id: str | None = Query(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Category]:
    # check if return value is a list of categories or a list of exercises
    return category_service.get_categories_by_athlete_id(athlete_id, db)


@router.get(
    '/{id}', response_model=CategoryFullResponseSchema, status_code=status.HTTP_200_OK
)
async def get_category_by_id(
    id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Category:
    return category_service.get_category_by_id(id, db)
