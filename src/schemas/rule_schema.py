from datetime import date
from typing import Optional
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
    gender: Optional[Gender] = None
    from_age: Optional[int] = None
    to_age: Optional[int] = None
    bronze: Optional[str] = None
    silver: Optional[str] = None
    gold: Optional[str] = None
    year: Optional[date] = None

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

