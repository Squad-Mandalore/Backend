import uuid
from datetime import date
from typing import Optional

from src.models.models import Gender
from src.schemas.user_schema import UserSchema, UserDtoSchema, UpdateDtoSchema


class AthleteDtoSchema(UserDtoSchema):
    birthday: date
    gender: Gender
    has_disease: bool
    trainer_id: Optional[str]

class AthleteUpadteDtoSchema(UpdateDtoSchema):
    birthday: Optional[date] = None
    gender: Optional[Gender] = None
    has_disease: Optional[bool] = None
    trainer_id: Optional[str] = None


class AthleteSchema(UserSchema):
    # model_config = ConfigDict()
    birthday: date
    gender: Gender
    has_disease: bool
    trainer_id: Optional[uuid.UUID]
