from datetime import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.models.user_model import Athlete

class Completes(Base):
    __tablename__ = "completes"
    athlete_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("athlete.id"), primary_key=True)
    exercise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exercise.id"), primary_key=True)
    tracked_at: Mapped[datetime]
    completed_at: Mapped[datetime]
    result: Mapped[str]
    points: Mapped[int]
    dbs: Mapped[bool] = mapped_column(default=False)

    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="completes")
