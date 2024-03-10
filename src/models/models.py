from datetime import date, datetime
import enum
from typing import Optional
import uuid

from sqlalchemy import BLOB, CheckConstraint, Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.password_service import hash_and_spice_password

def get_uuid() -> str:
    return str(uuid.uuid4())

class Base(DeclarativeBase):
    pass

class Gender(enum.Enum):
    MALE = 'm'
    FEMALE = 'f'
    DIVERSE = 'd'

class User(Base):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(primary_key=True, default=get_uuid)
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

    def __init__(self, username: str, email: str, unhashed_password: str, firstname: str, lastname: str):
        now = datetime.now()
        hashed_password, salt = hash_and_spice_password(unhashed_password)
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.firstname = firstname
        self.lastname = lastname
        self.salt = salt
        self.created_at = now
        self.last_edited_at = now
        self.last_password_change = now


class Administrator(User):
    __tablename__ = "administrator"
    id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)
    uses_otp: Mapped[bool] = mapped_column(default=False)

    codes: Mapped[list["BackupCode"]] = relationship(back_populates="administrator")

    __mapper_args__ = {"polymorphic_identity": "administrator"}

    def __init__(self, username: str, email: str, unhashed_password: str, firstname: str, lastname: str,
                 uses_otp: bool):
        super().__init__(username, email, unhashed_password, firstname, lastname)
        uses_otp = uses_otp


class Trainer(User):
    __tablename__ = "trainer"
    id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)
    uses_otp: Mapped[bool]
    birthday: Mapped[Optional[date]]

    athletes: Mapped[list["Athlete"]] = relationship(back_populates="trainer",
                                                     primaryjoin="Trainer.id==Athlete.trainer_id")
    codes: Mapped[list["BackupCode"]] = relationship(back_populates="trainer")

    __mapper_args__ = {"polymorphic_identity": "trainer"}

    def __init__(self, username: str, email: str, unhashed_password: str, firstname: str, lastname: str, birthday: Optional[date],
                 uses_otp: bool = False):
        super().__init__(username, email, unhashed_password, firstname, lastname)
        self.uses_otp = uses_otp
        self.birthday = birthday


class Athlete(User):
    __tablename__ = "athlete"
    id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)
    birthday: Mapped[date]
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    has_disease: Mapped[bool]
    trainer_id: Mapped[str] = mapped_column(ForeignKey("trainer.id"))

    trainer: Mapped["Trainer"] = relationship(back_populates="athletes", primaryjoin="Trainer.id==Athlete.trainer_id")
    completes: Mapped[list["Completes"]] = relationship(back_populates="athlete")
    certificates: Mapped[list["Certificate"]] = relationship()

    __mapper_args__ = {"polymorphic_identity": "athlete"}

    def __init__(self, username: str, email: str, unhashed_password: str, firstname: str, lastname: str,
                 birthday: date, trainer_id: str, has_disease: bool = False, gender: Gender = Gender.DIVERSE):
        super().__init__(username, email, unhashed_password, firstname, lastname)
        self.birthday = birthday
        self.trainer_id = trainer_id
        self.gender = gender
        self.has_disease = has_disease


class Category(Base):
    __tablename__ = "category"
    id: Mapped[str] = mapped_column(primary_key=True, default=get_uuid)
    title: Mapped[str]

    exercises: Mapped[list["Exercise"]] = relationship(back_populates="category",
                                                       primaryjoin="Category.id==Exercise.category_id")

    def __init__(self, title: str):
        self.title = title


class Certificate(Base):
    __tablename__ = "certificate"
    id: Mapped[str] = mapped_column(primary_key=True, default=get_uuid)
    athlete_id: Mapped[str] = mapped_column(ForeignKey("athlete.id"), primary_key=True)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.now)
    uploaded_by: Mapped[str] = mapped_column(ForeignKey("trainer.id"))
    title: Mapped[str]
    blob: Mapped[bytes] = mapped_column(BLOB)

    athlete: Mapped["Athlete"] = relationship(back_populates="certificates")
    uploader: Mapped["Trainer"] = relationship()

    def __init__(self, athlete_id: str, uploader: str, title: str, blob: bytes):
        self.athlete_id = athlete_id
        self.uploaded_by = uploader
        self.title = title
        self.blob = blob


class BackupCode(Base):
    __tablename__ = "backup_code"
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)
    code: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]

    administrator: Mapped["Administrator"] = relationship("Administrator", back_populates="codes")
    trainer: Mapped["Trainer"] = relationship("Trainer", back_populates="codes")

    def __init__(self, user_id: str, code: str):
        self.user_id = user_id
        self.code = code
        self.created_at = datetime.now()


class Exercise(Base):
    __tablename__ = "exercise"
    id: Mapped[str] = mapped_column(primary_key=True, default=get_uuid)
    title: Mapped[str]
    category_id: Mapped[str] = mapped_column(ForeignKey("category.id"))
    from_age: Mapped[int]
    to_age: Mapped[int]

    category: Mapped["Category"] = relationship(back_populates="exercises",
                                                primaryjoin="Category.id==Exercise.category_id")

    __table_args__ = (
        CheckConstraint('from_age < to_age'),
    )

    def __init__(self, title: str, category_id: str, from_age: int, to_age: int):
        self.title = title
        self.category_id = category_id
        self.from_age = from_age
        self.to_age = to_age


class Completes(Base):
    __tablename__ = "completes"
    athlete_id: Mapped[str] = mapped_column(ForeignKey("athlete.id"), primary_key=True)
    exercise_id: Mapped[str] = mapped_column(ForeignKey("exercise.id"), primary_key=True)
    tracked_at: Mapped[datetime]
    completed_at: Mapped[datetime]
    result: Mapped[str]
    points: Mapped[int]
    dbs: Mapped[bool] = mapped_column(default=False)

    athlete: Mapped["Athlete"] = relationship()
    exercise: Mapped["Exercise"] = relationship()

    def __init__(self, athlete_id: str, exercise_id: str, tracked_at: datetime, completed_at: datetime, result: str,
                 points: int, dbs: bool = False):
        self.athlete_id = athlete_id
        self.exercise_id = exercise_id
        self.tracked_at = tracked_at
        self.completed_at = completed_at
        self.result = result
        self.points = points
        self.dbs = dbs


class Rule(Base):
    __tablename__ = "rule"
    id: Mapped[str] = mapped_column(primary_key=True, default=get_uuid)
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    from_age: Mapped[int]
    to_age: Mapped[int]
    bronze: Mapped[str]
    silver: Mapped[str]
    gold: Mapped[str]
    year: Mapped[date]

    exercise_id: Mapped[str] = mapped_column(ForeignKey("exercise.id"))

    exercise: Mapped[Exercise] = relationship()

    __table_args__ = (
        CheckConstraint('from_age < to_age'),
    )

    def __init__(self, gender: Gender, from_age: int, to_age: int, bronze: str, silver: str, gold: str, year: date,
                 exercise_id: str):
        self.gender = gender
        self.from_age = from_age
        self.to_age = to_age
        self.bronze = bronze
        self.silver = silver
        self.gold = gold
        self.year = year
        self.exercise_id = exercise_id
