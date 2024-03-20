from datetime import date
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


class AthleteResponseSchema(UserResponseSchema):
    birthday: date
    gender: Gender
    has_disease: bool
    trainer_id: str

class CategoryModel(BaseModel):
    id: str
    title: str

class ExerciseModel(BaseModel):
    id: str
    title: str
    category: CategoryModel  # Nested CategoryModel
    from_age: int
    to_age: int

class CompletesModel(BaseModel):
    athlete_id: str
    exercise_id: ExerciseModel
    tracked_at: date
    completed_at: Optional[date]
    result: str
    points: int
    dbs: bool

class CertificateModel(BaseModel):
    id: str
    athlete_id: str
    uploaded_at: date
    uploaded_by: str
    title: str
    blob: str

class AthleteFullResponseSchema(AthleteResponseSchema):
    completes: list[CompletesModel]
    certificates: list[CertificateModel]

