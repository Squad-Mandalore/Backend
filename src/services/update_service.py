from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.models import Base


def update_properties(athleteDb: Base, schema: BaseModel, db: Session):
    now = datetime.now()
    for attr, value in schema.__dict__.items():
        if value is not None:
            setattr(athleteDb, attr, value)
    athleteDb.last_edited_at = now
    db.commit()