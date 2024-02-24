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

class AthleteUpdateSchema(UpdateDtoSchema):
    birthday: Optional[str]
    trainer_id: Optional[str]
    has_disease: Optional[bool]
    gender: Optional[str]
class AthleteSchema(UserSchema):
    # model_config = ConfigDict()
    birthday: date
    gender: Gender
    has_disease: bool
    trainer_id: Optional[uuid.UUID]
