from datetime import date
from typing import Optional
from pydantic import BaseModel

from src.models.models import Gender


class CategoryPostSchema(BaseModel):
    title: str

class CategoryPatchSchema(BaseModel):
    title: Optional[str] = None

class CategoryRuleResponseSchema(BaseModel):
    id: str
    gender: Gender
    from_age: int
    to_age: int
    bronze: str
    silver: str
    gold: str
    year: date

class CategoryResponseSchema(CategoryPostSchema):
    id: str

class CategoryFullResponseSchema(CategoryResponseSchema):
    exercises: list[CategoryResponseSchema]

class CategoryExerciseFullResponseSchema(CategoryResponseSchema):
    rules: list[CategoryRuleResponseSchema]

class CategoryVeryFullResponseSchema(CategoryResponseSchema):
    exercises: list[CategoryExerciseFullResponseSchema]


