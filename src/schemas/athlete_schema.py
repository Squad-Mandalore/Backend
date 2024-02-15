from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.models.models import Gender, Trainer

class AthleteDtoSchema(BaseModel):
    username: str
    email: str
    hashed_password: str
    salt: str
    firstname: str
    lastname: str
    birthday: date
    gender: Gender
    has_disease: bool
    trainer_id: Optional[int]
class AthleteSchema(AthleteDtoSchema):
    # model_config = ConfigDict()
    id: str

