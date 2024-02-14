from pydantic import BaseModel


class UserSchema(BaseModel):
    # model_config = ConfigDict()
    id: str
    password: str
