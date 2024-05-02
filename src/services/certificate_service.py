from typing import cast

from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Base
from src.models.models import Certificate
from src.schemas.certificate_schema import CertificatePostSchema, CertificatePatchSchema
from src.services import update_service


def create_certificate(athlete_id, title, blob: UploadFile, user_id: str, db: Session) -> Certificate:
    blob_data = blob.file.read()
    certificate_post_schema = CertificatePostSchema(
        athlete_id=athlete_id,
        title=title,
        blob=blob_data
    )
    certificate_dict = certificate_post_schema.model_dump(exclude_unset=True)
    certificates = Certificate(**certificate_dict, uploader=user_id)
    database_utils.add(certificates, db)
    return certificates


def get_certificates_by_id(id: str, db: Session) -> Certificate:
    certificate: Certificate | None = db.get(Certificate, id)

    if certificate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")
    return certificate

# At the moment not in use, can be marked as deprecated if patch is not in use?
def update_certificate(id: str, certificate_patch_schema: CertificatePatchSchema, db: Session) -> Certificate:
    certificate: Base | None = db.get(Certificate, id)

    if certificate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")

    update_service.update_properties(certificate, certificate_patch_schema)
    return cast(Certificate, certificate)


def delete_certificate(id: str, db: Session) -> None:
    return database_utils.delete(Certificate, id, db)
