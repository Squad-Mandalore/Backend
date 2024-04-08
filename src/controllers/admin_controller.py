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
    prefix="/admins",
    # documentation tag
    tags=["admins"],
    # default response
    #responses={404: {"route": "Not found"}},
)

@router.get("/all", response_model=list[AdminResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_admins(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Admin]:
    return admin_service.get_all_admins(db)

@router.get("/{id}", response_model=AdminResponseSchema, status_code=status.HTTP_200_OK)
async def get_admin(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Admin:
    return admin_service.get_admin_by_id(id, db)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_admin(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    return admin_service.delete_admin(id, db)

@router.post("/", response_model=AdminResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_admin(admin_post_schema: AdminPostSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Admin:
    return admin_service.create_admin(admin_post_schema, db)

@router.patch("/{id}", response_model=AdminResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_admin(id: str, admin_patch_schema: AdminPatchSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Base:
    return admin_service.update_admin(id, admin_patch_schema, db)
