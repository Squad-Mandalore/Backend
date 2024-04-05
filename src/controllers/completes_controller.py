from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Completes, User
from src.schemas.completes_schema import CompletesPatchSchema, CompletesPostSchema, CompletesResponseSchema
from src.services import completes_service
from src.services.auth_service import get_current_user


router = APIRouter(
    # routing prefix
    prefix="/completes",
    # documentation tag
    tags=["completes"],
    # default response
    #responses={404: {"route": "Not found"}},
)

# completes routes
@router.get("/", response_model=list[CompletesResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_completes(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Completes]:
    return completes_service.get_all_completes(db)

@router.get("/{id}", response_model=CompletesResponseSchema, status_code=status.HTTP_200_OK)
async def get_completes(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Completes:
    return completes_service.get_completes_by_id(id, db)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_ahtlete(id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    return completes_service.delete_completes(id, db)

@router.post("/", response_model=CompletesResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_completes(completes_post_schema: CompletesPostSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Completes:
    return completes_service.create_completes(completes_post_schema, user.id, db)

@router.patch("/{id}", response_model=CompletesResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_completes(id: str, completes_patch_schema: CompletesPatchSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Completes:
    return completes_service.update_completes(id, completes_patch_schema, user.id, db)
