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

class AthletePatchSchema(UserPatchSchema):
    birthday: Optional[date] = None
    gender: Optional[Gender] = None

class AthleteResponseSchema(UserResponseSchema):
    birthday: date
    gender: Gender
    trainer: TrainerResponseSchema

class AthleteFullResponseSchema(AthleteResponseSchema):
    completes: list[CompletesResponseSchema]
    certificates: list[CertificateResponseSchema]

