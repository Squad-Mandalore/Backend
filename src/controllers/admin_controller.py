from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Administrator
from src.models.models import User
from src.schemas.admin_schema import AdminPatchSchema
from src.schemas.admin_schema import AdminResponseSchema
from src.services import admin_service
from src.services.auth_service import get_current_user


router = APIRouter(
    # routing prefix
    prefix='/admins',
    # documentation tag
    tags=['admins'],
    # default response
    # responses={404: {"route": "Not found"}},
)


@router.get(
    '/', response_model=list[AdminResponseSchema], status_code=status.HTTP_200_OK
)
async def get_all_admins(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[Administrator]:
    return admin_service.get_all_admins(db)


@router.get('/{id}', response_model=AdminResponseSchema, status_code=status.HTTP_200_OK)
async def get_admin(
    id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Administrator:
    return admin_service.get_admin_by_id(id, db)


# @router.delete("/{id}", status_code=status.HTTP_200_OK)
# async def delete_admin(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
#    return admin_service.delete_admin(id, db)

# @router.post("/", response_model=AdminResponseSchema, status_code=status.HTTP_201_CREATED)
# async def create_admin(admin_post_schema: AdminPostSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Administrator:
#    return admin_service.create_admin(admin_post_schema, db)


@router.patch(
    '/{id}', response_model=AdminResponseSchema, status_code=status.HTTP_202_ACCEPTED
)
async def update_admin(
    id: str,
    admin_patch_schema: AdminPatchSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Administrator:
    return admin_service.update_admin(id, admin_patch_schema, db)
