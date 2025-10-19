from typing import cast

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Base
from src.models.models import Exercise
from src.schemas.exercise_schema import ExercisePatchSchema
from src.schemas.exercise_schema import ExercisePostSchema
from src.services import update_service


def create_exercise(exercise_post_schema: ExercisePostSchema, db: Session) -> Exercise:
    exercise_dict = exercise_post_schema.model_dump(exclude_unset=True)
    exercise = Exercise(**exercise_dict)
    database_utils.add(exercise, db)
    return exercise


def get_exercise_by_id(id: str, db: Session) -> Exercise:
    exercise: Base | None = db.get(Exercise, id)

    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Exercise not found'
        )

    return cast(Exercise, exercise)


def update_exercise(
    id: str, exercise_patch_schema: ExercisePatchSchema, db: Session
) -> Exercise:
    exercise: Base | None = db.get(Exercise, id)

    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Exercise not found'
        )

    update_service.update_properties(exercise, exercise_patch_schema)
    db.commit()
    return cast(Exercise, exercise)


def delete_exercise(id: str, db: Session) -> None:
    return database_utils.delete(Exercise, id, db)


def get_all_exercises(db: Session) -> list[Exercise]:
    return cast(list[Exercise], database_utils.get_all(Exercise, db))
