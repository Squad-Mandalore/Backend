from typing import Optional
from pydantic import BaseModel

from src.schemas.category_schema import CategoryResponseSchema


class ExercisePostSchema(BaseModel):
    title: str
    category_id: str
    from_age: int
    to_age: int

class ExercisePatchSchema(BaseModel):
    title: Optional[str]
    category_id: Optional[str]
    from_age: Optional[int]
    to_age: Optional[int]

class ExerciseResponseSchema(BaseModel):
    id: str
    title: str
    category: CategoryResponseSchema  # Nested CategoryModel
    from_age: int
    to_age: int
