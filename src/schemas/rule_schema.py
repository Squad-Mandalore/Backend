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
    gender: Optional[Gender]
    from_age: Optional[int]
    to_age: Optional[int]
    bronze: Optional[str]
    silver: Optional[str]
    gold: Optional[str]
    year: Optional[date]
    exercise_id: Optional[str]

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

