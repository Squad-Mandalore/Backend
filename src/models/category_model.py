import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.models.exercise_model import Exercise

class Category(Base):
    __tablename__ = "category"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str]

    exercises: Mapped[list["Exercise"]] = relationship(back_populates="category", primaryjoin="Category.id==Exercise.category_id")
