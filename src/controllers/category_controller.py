from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Category, User
from src.schemas.category_schema import CategoryPatchSchema, CategoryPostSchema, CategoryResponseSchema
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

@router.get("/all", response_model=list[CategoryResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_categorys(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Category]:
    return category_service.get_all_categorys(db)

@router.get("/{id}", response_model=CategoryResponseSchema, status_code=status.HTTP_200_OK)
async def get_category(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Category:
    return category_service.get_category_by_id(id, db)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_ahtlete(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    return category_service.delete_category(id, db)

@router.post("/", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_category(category_post_schema: CategoryPostSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Category:
    return category_service.create_category(category_post_schema, db)

@router.patch("/{id}", response_model=CategoryResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_category(id: str, category_patch_schema: CategoryPatchSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Category:
    return category_service.update_category(id, category_patch_schema, db)
