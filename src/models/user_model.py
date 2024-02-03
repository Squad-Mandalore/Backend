from datetime import date, datetime
import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base

class Gender(enum.Enum):
    MALE = 'm'
    FEMALE = 'f'
    DIVERSE = 'd'

class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    username: Mapped[str]= mapped_column(unique=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    firstname: Mapped[str]
    lastname: Mapped[str]
    created_at: Mapped[datetime]
    last_password_change: Mapped[datetime]
    last_edited_at: Mapped[datetime]
    type: Mapped[str]

    __mapper_args__ = { "polymorphic_on": "type", "polymorphic_abstract": True}

class Administrator(User):
    __tablename__ = "administrator"
    uses_otp: Mapped[bool]
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)

    __mapper_args__ = { "polymorphic_identity": "administrator" }

class Trainer(User):
    __tablename__ = "trainer"
    birthday: Mapped[date] = mapped_column(nullable=True)
    uses_otp: Mapped[bool]
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)

    athletes: Mapped[list["Athlete"]] = relationship(back_populates="trainer", primaryjoin="Trainer.id==Athlete.trainer_id")

    __mapper_args__ = { "polymorphic_identity": "trainer" }

class Athlete(User):
    __tablename__ = "athlete"
    birthday: Mapped[date]
    gender: Mapped[Gender] = mapped_column(Enum(Gender), default=Gender.DIVERSE)
    has_disease: Mapped[bool] = mapped_column(default=False)
    trainer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("trainer.id"))
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)

    trainer: Mapped["Trainer"] = relationship(back_populates="athletes", primaryjoin="Trainer.id==Athlete.trainer_id")

    __mapper_args__ = { "polymorphic_identity": "athlete" }
