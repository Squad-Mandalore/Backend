from datetime import date

from pydantic import BaseModel

from src.models.models import Gender
from src.schemas.certificate_schema import CertificateResponseSchema
from src.schemas.exercise_schema import ExerciseResponseSchema
from src.schemas.trainer_schema import TrainerResponseSchema
from src.schemas.user_schema import UserPatchSchema, UserPostSchema, UserResponseSchema


class AthletePostSchema(UserPostSchema):
    birthday: date
    gender: Gender


class AthletePatchSchema(UserPatchSchema):
    birthday: date | None = None
    gender: Gender | None = None


class AthleteResponseSchema(UserResponseSchema):
    birthday: date
    gender: Gender
    trainer: TrainerResponseSchema


class AthleteCompletesResponseSchema(BaseModel):
    athlete_id: str
    exercise: ExerciseResponseSchema
    tracked_at: date
    tracked_by: str
    trainer: TrainerResponseSchema
    result: str
    points: int


class AthleteFullResponseSchema(AthleteResponseSchema):
    completes: list[AthleteCompletesResponseSchema]
    certificates: list[CertificateResponseSchema]
