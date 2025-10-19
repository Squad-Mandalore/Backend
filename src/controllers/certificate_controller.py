import base64

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from src.database.database_utils import get_db
from src.models.models import Certificate, User
from src.schemas.certificate_schema import (
    CertificateResponseSchema,
    CertificateSingleResponseSchema,
)
from src.services import certificate_service
from src.services.auth_service import get_current_user

router = APIRouter(
    # routing prefix
    prefix='/certificates',
    # documentation tag
    tags=['certificates'],
    # default response
    # responses={404: {"route": "Not found"}},
)


@router.get(
    '/{id}',
    response_model=CertificateSingleResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_certificates(
    id: str, db: Session = Depends(get_db)
) -> CertificateSingleResponseSchema:
    certificate = certificate_service.get_certificates_by_id(id, db)
    certificate_data = CertificateSingleResponseSchema(
        blob=base64.b64encode(certificate.blob).decode('utf-8'), title=certificate.title
    )
    return certificate_data


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_certificate(id: str, db: Session = Depends(get_db)) -> None:
    return certificate_service.delete_certificate(id, db)


@router.post(
    '/', response_model=CertificateResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_certificate(
    blob: UploadFile = File(...),
    athlete_id: str = Form(...),
    title: str = Form(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Certificate:
    return certificate_service.create_certificate(athlete_id, title, blob, user.id, db)
