import uuid
from datetime import datetime

from pydantic import BaseModel

class UserDtoSchema(BaseModel):
    username: str
    email: str
    password: str
    firstname: str
    lastname: str


class UserSchema(BaseModel):
    # model_config = ConfigDict()
    id: uuid.UUID
    username: str
    email: str
    firstname: str
    lastname: str
    created_at: datetime
    last_password_change: datetime
    last_edited_at: datetime
