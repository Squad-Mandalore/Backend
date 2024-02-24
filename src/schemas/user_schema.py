import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class UserDtoSchema(BaseModel):
    username: str
    email: str
    unhashed_password: str
    firstname: str
    lastname: str

class UpdateDtoSchema(BaseModel):
    username: Optional[str]
    email: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
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
