from datetime import date

from pydantic import BaseModel

from src.models.models import Gender
from src.schemas.category_schema import CategoryResponseSchema


class RulePostSchema(BaseModel):
    gender: Gender
    from_age: int
    to_age: int
    bronze: str
    silver: str
    gold: str
    year: date
    exercise_id: str


class RulePatchSchema(BaseModel):
    gender: Gender | None = None
    from_age: int | None = None
    to_age: int | None = None
    bronze: str | None = None
    silver: str | None = None
    gold: str | None = None
    year: date | None = None


class RuleExerciseResponseSchema(BaseModel):
    id: str
    title: str
    category: CategoryResponseSchema


class RuleResponseSchema(BaseModel):
    id: str
    gender: Gender
    from_age: int
    to_age: int
    bronze: str
    silver: str
    gold: str
    year: date
    exercise: RuleExerciseResponseSchema
