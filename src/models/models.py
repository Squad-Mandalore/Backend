from datetime import date, datetime
import enum
from typing import Optional
import uuid

from sqlalchemy import BLOB, CheckConstraint, Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

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

    def __init__(self, username: str, email: str, hashed_password: str, firstname: str, lastname: str, salt: str):
        now = datetime.now()
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
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    uses_otp: Mapped[bool] = mapped_column(default=False)

    codes: Mapped[list["Code"]] = relationship(back_populates="administrator")

    __mapper_args__ = {"polymorphic_identity": "administrator"}

    def __init__(self, username: str, email: str, hashed_password: str, firstname: str, lastname: str, salt: str, uses_otp: bool):
        super().__init__(username, email, hashed_password, firstname, lastname, salt)
        uses_otp = uses_otp

class Trainer(User):
    __tablename__ = "trainer"
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    uses_otp: Mapped[bool] = mapped_column(default=False)
    birthday: Mapped[Optional[date]]

    athletes: Mapped[list["Athlete"]] = relationship(back_populates="trainer", primaryjoin="Trainer.id==Athlete.trainer_id")
    codes: Mapped[list["Code"]] = relationship(back_populates="trainer")

    __mapper_args__ = {"polymorphic_identity": "trainer"}

    def __init__(self, username: str, email: str, hashed_password: str, firstname: str, lastname: str, salt: str, uses_otp: bool, birthday: Optional[date]):
        super().__init__(username, email, hashed_password, firstname, lastname, salt)
        self.uses_otp = uses_otp
        self.birthday = birthday

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

    def __init__(self, username: str, email: str, hashed_password: str, firstname: str, lastname: str, salt: str, birthday: date, gender: Gender, has_disease: bool, trainer: Trainer):
        super().__init__(username, email, hashed_password, firstname, lastname, salt)
        self.birthday = birthday
        self.trainer = trainer
        self.gender = gender
        self.has_disease = has_disease

class Category(Base):
    __tablename__ = "category"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str]

    exercises: Mapped[list["Exercise"]] = relationship(back_populates="category", primaryjoin="Category.id==Exercise.category_id")

    def __init__(self, title: str):
        self.title = title

class Certificate(Base):
    __tablename__ = "certificate"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("athlete.id"), primary_key=True)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.now)
    title: Mapped[str]
    blob: Mapped[bytes] = mapped_column(BLOB)

    athlete: Mapped["Athlete"] = relationship()

    def __init__(self, athlete: Athlete, title: str, blob: bytes):
        self.athlete = athlete
        self.title = title
        self.blob = blob

class Code(Base):
    __tablename__ = "codes"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    code: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]

    administrator: Mapped["Administrator"] = relationship("Administrator", back_populates="codes")
    trainer: Mapped["Trainer"] = relationship("Trainer", back_populates="codes")

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

    def __init__(self, title: str, category: Category, from_age: int, to_age: int):
        self.title = title
        self.category = category
        self.from_age = from_age
        self.to_age = to_age

class Completes(Base):
    __tablename__ = "completes"
    athlete_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("athlete.id"), primary_key=True)
    exercise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exercise.id"), primary_key=True)
    tracked_at: Mapped[datetime]
    completed_at: Mapped[datetime]
    result: Mapped[str]
    points: Mapped[int]
    dbs: Mapped[bool] = mapped_column(default=False)

    athlete: Mapped["Athlete"] = relationship()
    exercise: Mapped["Exercise"] = relationship()

    def __init__(self, athlete: Athlete, exercise: Exercise, tracked_at: datetime, completed_at: datetime, result: str, points: int, dbs: bool):
        self.athlete = athlete
        self.exercise = exercise
        self.tracked_at = tracked_at
        self.completed_at = completed_at
        self.result = result
        self.points = points
        self.dbs = dbs

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

    exercise: Mapped[Exercise] = relationship()

    __table_args__ = (
        CheckConstraint('from_age < to_age'),
    )

    def __init__(self, gender: Gender, from_age: int, to_age: int, bronze: str, silver: str, gold: str, year: date, exercise: Exercise):
        self.gender = gender
        self.from_age = from_age
        self.to_age = to_age
        self.bronze = bronze
        self.silver = silver
        self.gold = gold
        self.year = year
        self.exercise = exercise
