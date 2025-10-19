from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Base, Trainer, User
from src.schemas.trainer_schema import (
    TrainerPatchSchema,
    TrainerPostSchema,
    TrainerResponseSchema,
)
from src.services import trainer_service
from src.services.auth_service import get_current_user

router = APIRouter(
    # routing prefix
    prefix='/trainers',
    # documentation tag
    tags=['trainers'],
    # default response
    # responses={404: {"route": "Not found"}},
)


@router.get(
    '/', response_model=list[TrainerResponseSchema], status_code=status.HTTP_200_OK
)
async def get_all_trainers(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[Trainer]:
    return trainer_service.get_all_trainers(db)


@router.get(
    '/{id}', response_model=TrainerResponseSchema, status_code=status.HTTP_200_OK
)
async def get_trainer(
    id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Trainer:
    return trainer_service.get_trainer_by_id(id, db)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_trainer(
    id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> None:
    return trainer_service.delete_trainer(id, db)


@router.post(
    '/', response_model=TrainerResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_trainer(
    trainer_post_schema: TrainerPostSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Trainer:
    return trainer_service.create_trainer(trainer_post_schema, db)


@router.patch(
    '/{id}', response_model=TrainerResponseSchema, status_code=status.HTTP_202_ACCEPTED
)
async def update_trainer(
    id: str,
    trainer_patch_schema: TrainerPatchSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Base:
    return trainer_service.update_trainer(id, trainer_patch_schema, db)
