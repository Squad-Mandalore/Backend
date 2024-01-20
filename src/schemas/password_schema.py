from pydantic import BaseModel


class PasswordSchema(BaseModel):
    password: str
