import uuid
from datetime import date
from typing import Optional

from src.models.models import Gender
from src.schemas.user_schema import UserSchema, UserDtoSchema


class AthleteDtoSchema(UserDtoSchema):
    birthday: date
    gender: Gender
    has_disease: bool
    trainer_id: Optional[str]
class AthleteSchema(UserSchema):
    # model_config = ConfigDict()
    birthday: date
    gender: Gender
    has_disease: bool
    trainer_id: Optional[uuid.UUID]
