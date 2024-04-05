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

class CategoryResponseSchema(BaseModel):
    id: str
    title: str

class CategoryExerciseResponseSchema(BaseModel):
    id: str
    title: str
    from_age: int
    to_age: int

class CategoryFullResponseSchema(BaseModel):
    id: str
    title: str
    exercises: list[CategoryExerciseResponseSchema]

class CategoryExerciseFullResponseSchema(BaseModel):
    id: str
    title: str
    from_age: int
    to_age: int
    category: CategoryResponseSchema
    rules: list[CategoryRuleResponseSchema]

