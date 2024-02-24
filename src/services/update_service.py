from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.models import Base


def update_properties(obj: BaseModel, schema: BaseModel):
    now = datetime.now()
    update_fields = schema.dict(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(obj, field, value)
    obj.last_edited_at = now