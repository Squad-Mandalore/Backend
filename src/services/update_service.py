from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.models import Base



def update_properties(obj: Base, schema: BaseModel, db: Session):
    now = datetime.now()
    update_fields = schema.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(obj, field, value)
    setattr(obj, "last_edited_at", now)
    db.commit()
