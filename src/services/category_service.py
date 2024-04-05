from typing import cast
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.database import database_utils
from src.models.models import Base, Category
from src.schemas.category_schema import CategoryPatchSchema, CategoryPostSchema
from src.services import update_service


def create_category(category_post_schema: CategoryPostSchema, db: Session) -> Category:
    category_dict = category_post_schema.model_dump(exclude_unset=True)
    category = Category(**category_dict)
    database_utils.add(category, db)
    return category

def get_category_by_id(id: str, db: Session) -> Category:
    category: Base | None = db.get(Category, id)

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    return cast(Category, category)

def update_category(id: str, category_patch_schema: CategoryPatchSchema, db: Session) -> Category:
    category: Base | None = db.get(Category, id)

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_service.update_properties(category, category_patch_schema)
    db.commit()
    return cast(Category, category)

def delete_category(id: str, db: Session) -> None:
    return database_utils.delete(Category, id, db)

def get_all_categories(db: Session) -> list[Category]:
    return cast(list[Category], database_utils.get_all(Category, db))
