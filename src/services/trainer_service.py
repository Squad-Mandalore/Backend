from datetime import datetime
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT

from src.database import database_utils
from src.models.models import Base, Trainer, User
from src.schemas.trainer_schema import TrainerPatchSchema, TrainerPostSchema
from src.services import update_service


def create_trainer(trainer_post_schema: TrainerPostSchema, db: Session) -> Trainer:
    user_db: User | None = db.scalar(
        select(User).where(User.username == trainer_post_schema.username)
    )
    if user_db is not None:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_CONTENT, detail='Username already in use'
        )

    trainer_dict = trainer_post_schema.model_dump(exclude_unset=True)
    trainer = Trainer(**trainer_dict)
    database_utils.add(trainer, db)
    return trainer


def get_trainer_by_id(id: str, db: Session) -> Trainer:
    trainer: Base | None = db.get(Trainer, id)
    if trainer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Trainer not found'
        )

    return cast(Trainer, trainer)


def update_trainer(
    id: str, trainer_patch_schema: TrainerPatchSchema, db: Session
) -> Trainer:
    trainer: Trainer = get_trainer_by_id(id, db)
    if (
        trainer_patch_schema.username is not None
        and trainer.username != trainer_patch_schema.username
    ):
        user_db: User | None = db.scalar(
            select(User).where(User.username == trainer_patch_schema.username)
        )
        if user_db is not None:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Username already in use',
            )

    if trainer_patch_schema.unhashed_password is not None:
        update_service.update_password(trainer, trainer_patch_schema.unhashed_password)
        trainer_patch_schema.unhashed_password = None

    update_service.update_properties(trainer, trainer_patch_schema)
    trainer.last_edited_at = datetime.now()
    db.commit()
    return cast(Trainer, trainer)


def delete_trainer(id: str, db: Session) -> None:
    return database_utils.delete(Trainer, id, db)


def get_all_trainers(db: Session) -> list[Trainer]:
    return cast(list[Trainer], database_utils.get_all(Trainer, db))
