from pydantic import BaseModel

from src.models.models import Base

def update_properties(obj: Base, schema: BaseModel):
    update_fields = schema.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(obj, field, value)
