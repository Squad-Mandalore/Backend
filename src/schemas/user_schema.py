from datetime import datetime

from pydantic import BaseModel


class UserPostSchema(BaseModel):
    username: str
    email: str
    unhashed_password: str
    firstname: str
    lastname: str


class UserPatchSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    unhashed_password: str | None = None


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
    type: str
