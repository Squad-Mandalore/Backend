from datetime import date

from pydantic import BaseModel

from src.models.models import Gender, Trainer


class AthleteSchema(BaseModel):
    # model_config = ConfigDict()
    username: str
    email: str
    hashed_password: str
    firstname: str
    lastname: str
    salt: str
    birthday: date
    gender: Gender
    has_disease: bool
    trainer: Trainer