from typing import cast

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Base
from src.models.models import Certificate
from src.schemas.certificate_schema import CertificatePostSchema, CertificatePatchSchema
from src.services import update_service


def create_certificate(certificate_post_schema: CertificatePostSchema, db: Session) -> Certificate:
    certificate_dict = certificate_post_schema.model_dump(exclude_unset=True)
    certificates = Certificate(**certificate_dict)
    database_utils.add(certificates, db)
    return certificates


def get_certificates_by_id(id: str, db: Session) -> Certificate:
    certificate: Base | None = db.get(Certificate, id)

    if certificate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")

    return cast(Certificate, certificate)


def update_certificate(id: str, certificate_patch_schema: CertificatePatchSchema, db: Session) -> Certificate:
    completes: Base | None = db.get(Certificate, id)

    if completes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")

    update_service.update_properties(completes, certificate_patch_schema)
    return cast(Certificate, completes)


def delete_certificate(id: str, db: Session) -> None:
    return database_utils.delete(Certificate, id, db)


def get_all_certificates(db: Session) -> list[Certificate]:
    return cast(list[Certificate], database_utils.get_all(Certificate, db))
