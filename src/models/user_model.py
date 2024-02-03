from datetime import date, datetime
import enum
from typing import Optional
import uuid

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import Base
from src.models.code_model import Code
from src.models.complete_model import Completes

class Gender(enum.Enum):
    MALE = 'm'
    FEMALE = 'f'
    DIVERSE = 'd'

class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    firstname: Mapped[str]
    lastname: Mapped[str]
    created_at: Mapped[datetime]
    last_password_change: Mapped[datetime]
    last_edited_at: Mapped[datetime]
    type: Mapped[str]
    salt: Mapped[str]

    __mapper_args__ = {"polymorphic_on": "type", "polymorphic_abstract": True}

class Administrator(User):
    __tablename__ = "administrator"
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    uses_otp: Mapped[bool] = mapped_column(default=False)

    codes: Mapped[list["Code"]] = relationship("Codes", back_populates="administrator")

    __mapper_args__ = {"polymorphic_identity": "administrator"}

class Trainer(User):
    __tablename__ = "trainer"
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    uses_otp: Mapped[bool] = mapped_column(default=False)
    birthday: Mapped[Optional[date]]

    athletes: Mapped[list["Athlete"]] = relationship(back_populates="trainer", primaryjoin="Trainer.id==Athlete.trainer_id")
    codes: Mapped[list["Code"]] = relationship("Codes", back_populates="trainer")

    __mapper_args__ = {"polymorphic_identity": "trainer"}

class Athlete(User):
    __tablename__ = "athlete"
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    birthday: Mapped[date]
    gender: Mapped[Gender] = mapped_column(Enum(Gender), default=Gender.DIVERSE)
    has_disease: Mapped[bool] = mapped_column(default=False)
    trainer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("trainer.id"))

    trainer: Mapped["Trainer"] = relationship(back_populates="athletes", primaryjoin="Trainer.id==Athlete.trainer_id")
    exercises: Mapped[list["Completes"]] = relationship(back_populates="athlete")

    __mapper_args__ = {"polymorphic_identity": "athlete"}

