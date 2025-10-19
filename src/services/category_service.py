from datetime import date
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.database import database_utils
from src.models.models import Athlete, Base, Category, Exercise, Rule
from src.schemas.category_schema import CategoryPatchSchema, CategoryPostSchema
from src.services import update_service


def create_category(category_post_schema: CategoryPostSchema, db: Session) -> Category:
    category_dict = category_post_schema.model_dump(exclude_unset=True)
    category = Category(**category_dict)
    database_utils.add(category, db)
    return category


def get_category_by_id(category_id: str, db: Session) -> Category:
    category: Category | None = db.get(Category, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Category not found'
        )
    return category


def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()


def get_categories_by_athlete_id(athlete_id: str | None, db: Session) -> list[Category]:
    if athlete_id is None:
        return get_all_categories(db)

    athlete = db.get(Athlete, athlete_id)
    if athlete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Athlete not found'
        )

    athlete_age = date.today().year - athlete.birthday.year
    # Get all Exercises where the athlete's age and gender is within the age range of the Rule
    categories = (
        db.scalars(
            select(Category).options(
                joinedload(Category.exercises).joinedload(
                    Exercise.rules.and_(Rule.gender == athlete.gender)
                    .and_(Rule.from_age <= athlete_age)
                    .and_(Rule.to_age >= athlete_age)
                )
            )
        )
        .unique()
        .all()
    )

    for category in categories:
        filtered_exercises = [
            exercise for exercise in category.exercises if exercise.rules
        ]

        category.exercises = filtered_exercises

    return cast(list[Category], categories)


def update_category(
    id: str, category_patch_schema: CategoryPatchSchema, db: Session
) -> Category:
    category: Base | None = db.get(Category, id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Category not found'
        )

    update_service.update_properties(category, category_patch_schema)
    db.commit()
    return cast(Category, category)


def delete_category(id: str, db: Session) -> None:
    return database_utils.delete(Category, id, db)
