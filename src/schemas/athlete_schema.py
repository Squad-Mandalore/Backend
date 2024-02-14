from pydantic import BaseModel


class AthleteSchema(BaseModel):
    # model_config = ConfigDict()
    id: str
    password: str