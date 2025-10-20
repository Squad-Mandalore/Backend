from datetime import datetime

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


class CertificatePatchSchema(BaseModel):
    title: str | None = None
    blob: bytes | None = None


class CertificateSingleResponseSchema(BaseModel):
    title: str
    blob: str
