from pydantic import BaseModel


class CertificatePostSchema(BaseModel):
    athlete_id: str
    title: str

class CertificateResponseSchema(BaseModel):
    id: str
    athlete_id: str
    uploaded_at: datetime
    uploaded_by: str
    title: str
    blob: str