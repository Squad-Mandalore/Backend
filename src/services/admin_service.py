from datetime import datetime
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.database import database_utils
from src.models.models import Base, Administrator, User
from src.schemas.admin_schema import AdminPatchSchema, AdminPostSchema
from src.services import update_service

def create_admin(admin_post_schema: AdminPostSchema, db: Session) -> Administrator:
    user_db: User | None = db.scalar(select(User).where(User.username == admin_post_schema.username))
    if user_db is not None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Username already in use")

    admin_dict = admin_post_schema.model_dump(exclude_unset=True)
    admin = Administrator(**admin_dict)
    database_utils.add(admin, db)
    return admin

def get_admin_by_id(id: str, db: Session) -> Administrator:
    admin: Base | None = db.get(Administrator, id)
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Administrator not found")
    return cast(Administrator, admin)

def update_admin(id: str, admin_patch_schema: AdminPatchSchema, db: Session) -> Administrator:
    admin: Administrator = get_admin_by_id(id, db)
    if admin_patch_schema.username != None and admin.username != admin_patch_schema.username:
        user_db: User | None = db.scalar(select(User).where(User.username == admin_patch_schema.username))
        if user_db is not None:
            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Username already in use")

    if admin_patch_schema.unhashed_password != None:
        update_service.update_password(admin, admin_patch_schema.unhashed_password)
        admin_patch_schema.unhashed_password = None

    update_service.update_properties(admin, admin_patch_schema)
    setattr(admin, "last_edited_at", datetime.now())
    db.commit()
    return cast(Administrator, admin)

def delete_admin(id: str, db: Session) -> None:
    return database_utils.delete(Administrator, id, db)

def get_all_admins(db: Session) -> list[Administrator]:
    return cast(list[Administrator], database_utils.get_all(Administrator, db))
