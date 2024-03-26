from typing import cast

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Base, Trainer
from src.schemas.trainer_schema import TrainerPatchSchema, TrainerPostSchema
from src.services import update_service

def create_trainer(trainer_post_schema: TrainerPostSchema, db: Session) -> Trainer:
    trainer_dict = trainer_post_schema.model_dump(exclude_unset=True)
    trainer = Trainer(**trainer_dict)
    database_utils.add(trainer, db)
    return trainer

def get_trainer_by_id(id: str, db: Session) -> Trainer:
    trainer: Base | None = database_utils.get_by_id(Trainer, id, db)

    if trainer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trainer not found")
    return cast(Trainer, trainer)

def update_trainer(id: str, trainer_patch_schema: TrainerPatchSchema, db: Session) -> Trainer:
    trainer: Base | None = database_utils.get_by_id(Trainer, id, db)

    if trainer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trainer not found")
    update_service.update_properties(trainer, trainer_patch_schema, db)
    return cast(Trainer, trainer)

def delete_trainer(id: str, db: Session) -> None:
    return database_utils.delete(Trainer, id, db)

def get_all_trainers(db: Session) -> list[Trainer]:
    return cast(list[Trainer], database_utils.get_all(Trainer, db))
