from datetime import date
import uuid

from sqlalchemy import CheckConstraint, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.models.exercise_model import Exercise
from src.models.user_model import Gender

class Rule(Base):
    __tablename__ = "rule"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    from_age: Mapped[int]
    to_age: Mapped[int]
    bronze: Mapped[str]
    silver: Mapped[str]
    gold: Mapped[str]
    year: Mapped[date]

    exercise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exercise.id"))

    exercise: Mapped[Exercise] = relationship("Exercise", back_populates="rules")

    __table_args__ = (
        CheckConstraint('from_age < to_age'),
    )
