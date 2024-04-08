from datetime import date, datetime
import enum
import uuid

from fastapi import HTTPException, status
from sqlalchemy import BLOB, CheckConstraint, Enum, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Session
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

class Trainer(User):
    __tablename__ = "trainer"
    id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)

    athletes: Mapped[list["Athlete"]] = relationship(back_populates="trainer",
                                                     primaryjoin="Trainer.id==Athlete.trainer_id")
    certificates: Mapped[list["Certificate"]] = relationship(back_populates="uploader")

    __mapper_args__ = {"polymorphic_identity": "trainer"}

    def __init__(self, username: str, email: str, unhashed_password: str, firstname: str, lastname: str):
        super().__init__(username, email, unhashed_password, firstname, lastname)

class Administrator(Trainer):
    __tablename__ = "administrator"
    id: Mapped[str] = mapped_column(ForeignKey("trainer.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "administrator"}

    def __init__(self, username: str, email: str, unhashed_password: str, firstname: str, lastname: str):
        super().__init__(username, email, unhashed_password, firstname, lastname)

class Athlete(User):
    __tablename__ = "athlete"
    id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)
    birthday: Mapped[date]
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    trainer_id: Mapped[str] = mapped_column(ForeignKey("trainer.id"))

    trainer: Mapped["Trainer"] = relationship(back_populates="athletes", primaryjoin="Trainer.id==Athlete.trainer_id")
    completes: Mapped[list["Completes"]] = relationship(back_populates="athlete")
    certificates: Mapped[list["Certificate"]] = relationship(back_populates="athlete")

    __mapper_args__ = {"polymorphic_identity": "athlete"}

    def __init__(self, username: str, email: str, unhashed_password: str, firstname: str, lastname: str,
                 birthday: date, trainer_id: str, gender: Gender = Gender.DIVERSE):
        super().__init__(username, email, unhashed_password, firstname, lastname)
        self.birthday = birthday
        self.trainer_id = trainer_id
        self.gender = gender


class Category(Base):
    __tablename__ = "category"
    id: Mapped[str] = mapped_column(primary_key=True, default=get_uuid)
    title: Mapped[str]

    exercises: Mapped[list["Exercise"]] = relationship(back_populates="category")

    def __init__(self, title: str):
        self.title = title


class Certificate(Base):
    __tablename__ = "certificate"
    id: Mapped[str] = mapped_column(primary_key=True, default=get_uuid)
    athlete_id: Mapped[str] = mapped_column(ForeignKey("athlete.id"), primary_key=True)
    uploaded_at: Mapped[datetime]
    uploaded_by: Mapped[str] = mapped_column(ForeignKey("trainer.id"))
    title: Mapped[str]
    blob: Mapped[bytes] = mapped_column(BLOB)

    athlete: Mapped["Athlete"] = relationship(back_populates="certificates")
    uploader: Mapped["Trainer"] = relationship(back_populates="certificates")

    def __init__(self, athlete_id: str, uploader: str, title: str, blob: bytes):
        self.athlete_id = athlete_id
        self.uploaded_by = uploader
        self.title = title
        self.blob = blob
        self.uploaded_at = datetime.now()


class Exercise(Base):
    __tablename__ = "exercise"
    id: Mapped[str] = mapped_column(primary_key=True, default=get_uuid)
    title: Mapped[str]
    category_id: Mapped[str] = mapped_column(ForeignKey("category.id"))

    category: Mapped["Category"] = relationship(back_populates="exercises",
                                                primaryjoin="Category.id==Exercise.category_id")
    rules: Mapped[list["Rule"]] = relationship(back_populates="exercise")

    def __init__(self, title: str, category_id: str):
        self.title = title
        self.category_id = category_id

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

    exercise: Mapped["Exercise"] = relationship(back_populates="rules")

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

def calculate_points(athlete_id: str, exercise_id: str, tracked_at: date, result: str, db: Session) -> int:
    isbigger = True
    athlete: Athlete | None = db.get(Athlete, athlete_id)
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")
    athlete_age = tracked_at.year - athlete.birthday.year

    rule: Rule | None = db.scalar(select(Rule).where(Rule.exercise_id == exercise_id,
                                             Rule.gender == athlete.gender,
                                             Rule.from_age <= athlete_age,
                                             Rule.to_age >= athlete_age))

    if not rule:
        return 0

    if(rule.bronze > rule.gold):
        isbigger = False

    points = 0
    if isbigger:
        if result >= rule.gold:
            points = 3
        elif result >= rule.silver:
            points = 2
        elif result >= rule.bronze:
            points = 1
    else:
        if result <= rule.gold:
            points = 3
        elif result <= rule.silver:
            points = 2
        elif result <= rule.bronze:
            points = 1
    return points

class Completes(Base):
    __tablename__ = "completes"
    athlete_id: Mapped[str] = mapped_column(ForeignKey("athlete.id"), primary_key=True)
    exercise_id: Mapped[str] = mapped_column(ForeignKey("exercise.id"), primary_key=True)
    tracked_at: Mapped[date] = mapped_column(primary_key=True)
    tracked_by: Mapped[str] = mapped_column(ForeignKey("trainer.id"))
    result: Mapped[str]
    points: Mapped[int]

    athlete: Mapped["Athlete"] = relationship(back_populates="completes")
    exercise: Mapped["Exercise"] = relationship()
    trainer: Mapped["Trainer"] = relationship()

    def __init__(self, athlete_id: str, exercise_id: str, tracked_at: date, tracked_by: str, result: str, db: Session):
        self.athlete_id = athlete_id
        self.exercise_id = exercise_id
        self.tracked_at = tracked_at
        self.tracked_by = tracked_by
        self.result = result
        self.points = calculate_points(athlete_id, exercise_id, tracked_at, result, db)
