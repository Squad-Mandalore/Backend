from datetime import datetime
from pydantic import BaseModel


class CertificateSchema(BaseModel):
    id: str
    athlete_id: str
    uploaded_at: datetime
    uploaded_by: str
    title: str
    blob: str

