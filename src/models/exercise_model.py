import uuid

from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.models.category_model import Category

class Exercise(Base):
    __tablename__ = "exercise"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str]
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("category.id"))
    from_age: Mapped[int]
    to_age: Mapped[int]

    category: Mapped["Category"] = relationship(back_populates="exercises", primaryjoin="Category.id==Exercise.category_id")

    __table_args__ = (
        CheckConstraint('from_age < to_age'),
    )
