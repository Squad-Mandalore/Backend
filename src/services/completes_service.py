from typing import cast

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Base, Completes
from src.schemas.completes_schema import CompletesPatchSchema, CompletesPostSchema
from src.services import update_service


def create_completes(completes_post_schema: CompletesPostSchema, db: Session) -> Completes:
    completes_dict = completes_post_schema.model_dump(exclude_unset=True)
    completes = Completes(**completes_dict)
    database_utils.add(completes, db)
    return completes

def get_completes_by_id(id: str, db: Session) -> Completes:
    completes: Base | None = db.get(Completes, id)

    if completes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Completes not found")

    return cast(Completes, completes)

def update_completes(id: str, completes_patch_schema: CompletesPatchSchema, db: Session) -> Completes:
    completes: Base | None = db.get(Completes, id)

    if completes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Completes not found")

    update_service.update_properties(completes, completes_patch_schema, db)
    return cast(Completes, completes)

def delete_completes(id: str, db: Session) -> None:
    return database_utils.delete(Completes, id, db)

def get_all_completes(db: Session) -> list[Completes]:
    return cast(list[Completes], database_utils.get_all(Completes, db))
