from datetime import datetime
import uuid

from sqlalchemy import BLOB, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.models.user_model import Athlete

class Certificate(Base):
    __tablename__ = "certificate"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("athlete.id"), primary_key=True)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.now)
    title: Mapped[str]
    blob: Mapped[bytes] = mapped_column(BLOB)

    athlete: Mapped["Athlete"] = relationship(back_populates="certificates")
