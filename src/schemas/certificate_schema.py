from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
    blob: bytes


class CertificatePatchSchema(BaseModel):
    athlete_id: str
    title: Optional[str] = None
    blob: Optional[bytes] = None
