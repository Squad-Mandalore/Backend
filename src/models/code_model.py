from datetime import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.models.user_model import Administrator, Trainer

class Code(Base):
    __tablename__ = "codes"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    code: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]

    administrator: Mapped["Administrator"] = relationship("Administrator", back_populates="codes")
    trainer: Mapped["Trainer"] = relationship("Trainer", back_populates="codes")
