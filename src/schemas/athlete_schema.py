from datetime import date
from typing import Optional

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
    # model_config = ConfigDict()
    birthday: date
    gender: Gender
    has_disease: bool
    trainer_id: str
