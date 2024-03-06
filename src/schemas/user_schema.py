from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class UserPostSchema(BaseModel):
    username: str
    email: str
    unhashed_password: str
    firstname: str
    lastname: str

class UserPatchSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None

class UserResponseSchema(BaseModel):
    # model_config = ConfigDict()
    id: str
    username: str
    email: str
    firstname: str
    lastname: str
    created_at: datetime
    last_password_change: datetime
    last_edited_at: datetime
