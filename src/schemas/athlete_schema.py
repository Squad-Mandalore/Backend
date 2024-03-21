from datetime import date
from typing import Optional

from src.models.models import Gender
from src.schemas.certificate_schema import CertificateResponseSchema
from src.schemas.completes_schema import CompletesResponseSchema
from src.schemas.trainer_schema import TrainerResponseSchema
from src.schemas.user_schema import UserPatchSchema, UserPostSchema, UserResponseSchema


class AthletePostSchema(UserPostSchema):
    birthday: date
    gender: Gender
    has_disease: bool
    trainer_id: str

class AthletePatchSchema(UserPatchSchema):
    birthday: Optional[date] = None
    gender: Optional[Gender] = None
    has_disease: Optional[bool] = None
    trainer_id: Optional[str] = None

class AthleteResponseSchema(UserResponseSchema):
    birthday: date
    gender: Gender
    has_disease: bool
    trainer: TrainerResponseSchema

class AthleteFullResponseSchema(AthleteResponseSchema):
    completes: list[CompletesResponseSchema]
    certificates: list[CertificateResponseSchema]

