from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    password: str

    class Config:
        from_attributes = True
