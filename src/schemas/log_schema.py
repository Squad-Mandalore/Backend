from pydantic import BaseModel

class LogSchema(BaseModel):
    message: str
