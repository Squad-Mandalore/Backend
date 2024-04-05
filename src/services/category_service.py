from datetime import date
from typing import Sequence, cast
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from src.database import database_utils
from src.models.models import Athlete, Base, Category, Exercise, Rule
from src.schemas.category_schema import CategoryPatchSchema, CategoryPostSchema
from src.services import update_service
from src.logger.logger import logger


def create_category(category_post_schema: CategoryPostSchema, db: Session) -> Category:
    category_dict = category_post_schema.model_dump(exclude_unset=True)
    category = Category(**category_dict)
    database_utils.add(category, db)
    return category

def get_category_by_id(category_id: str | None, athlete_id: str | None, db: Session) -> list[Category] | list[Exercise]:

    if category_id is not None:
        category: Category | None = db.get(Category, category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return [category]

    if athlete_id is not None:
        athlete = db.get(Athlete, athlete_id)
        if athlete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")

        athlete_age = date.today().year - athlete.birthday.year
        # Get all Exercises where the athlete's age and gender is within the age range of the Rule
        exercises = db.query(Exercise).join(Rule).filter(
            Rule.gender == athlete.gender,
            Rule.from_age <= athlete_age,
            Rule.to_age >= athlete_age).all()

        return exercises



    return db.query(Category).all()


def update_category(id: str, category_patch_schema: CategoryPatchSchema, db: Session) -> Category:
    category: Base | None = db.get(Category, id)

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_service.update_properties(category, category_patch_schema)
    db.commit()
    return cast(Category, category)

def delete_category(id: str, db: Session) -> None:
    return database_utils.delete(Category, id, db)
