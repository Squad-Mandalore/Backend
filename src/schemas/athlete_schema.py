from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from src.models.models import Gender
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

class TrainerResponseSchema(UserResponseSchema):
    id: str
    uses_otp: bool
    birthday: Optional[date]

class AthleteResponseSchema(UserResponseSchema):
    birthday: date
    gender: Gender
    has_disease: bool
    trainer: TrainerResponseSchema

class CategorySchema(BaseModel):
    id: str
    title: str

class ExerciseSchema(BaseModel):
    id: str
    title: str
    category: CategorySchema  # Nested CategoryModel
    from_age: int
    to_age: int

class CompletesSchema(BaseModel):
    athlete_id: str
    exercise_id: ExerciseSchema
    tracked_at: datetime
    completed_at: Optional[datetime]
    result: str
    points: int
    dbs: bool

class CertificateSchema(BaseModel):
    id: str
    athlete_id: str
    uploaded_at: datetime
    uploaded_by: str
    title: str
    blob: str

class AthleteFullResponseSchema(AthleteResponseSchema):
    completes: list[CompletesSchema]
    certificates: list[CertificateSchema]

