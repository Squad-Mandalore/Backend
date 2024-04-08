from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.database import database_utils
from src.models.models import Base, Admin
from src.schemas.admin_schema import AdminPatchSchema, AdminPostSchema
from src.services import update_service

def create_admin(admin_post_schema: AdminPostSchema, db: Session) -> Admin:
    admin_db: Admin | None = db.scalar(select(Admin).where(Admin.username == admin_post_schema.username))
    if admin_db is not None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Username already in use")

    admin_dict = admin_post_schema.model_dump(exclude_unset=True)
    admin = Admin(**admin_dict)
    database_utils.add(admin, db)
    return admin

def get_admin_by_id(id: str, db: Session) -> Admin:
    admin: Base | None = db.get(Admin, id)
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return cast(Admin, admin)

def update_admin(id: str, admin_patch_schema: AdminPatchSchema, db: Session) -> Admin:
    admin: Base | None = db.get(Admin, id)
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    update_service.update_properties(admin, admin_patch_schema, db)
    return cast(Admin, admin)

def delete_admin(id: str, db: Session) -> None:
    return database_utils.delete(Admin, id, db)

def get_all_admins(db: Session) -> list[Admin]:
    return cast(list[Admin], database_utils.get_all(Admin, db))
