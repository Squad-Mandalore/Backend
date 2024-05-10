from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class CertificatePostSchema(BaseModel):
    athlete_id: str
    title: str
    blob: bytes


class CertificateResponseSchema(BaseModel):
    id: str
    athlete_id: str
    uploaded_at: datetime
    uploaded_by: str
    title: str


class CertificatePatchSchema(BaseModel):
    title: Optional[str] = None
    blob: Optional[bytes] = None


class CertificateSingleResponseSchema(BaseModel):
    title: str
    blob: str
