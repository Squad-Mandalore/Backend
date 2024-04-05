from typing import Optional
from pydantic import BaseModel

from src.schemas.category_schema import CategoryResponseSchema
from src.schemas.rule_schema import RuleResponseSchema


class ExercisePostSchema(BaseModel):
    title: str
    category_id: str
    from_age: int
    to_age: int
    category_id: str
    # rule_id: str

class ExercisePatchSchema(BaseModel):
    title: Optional[str] = None
    from_age: Optional[int] = None
    to_age: Optional[int] = None

class ExerciseResponseSchema(BaseModel):
    id: str
    title: str
    from_age: int
    to_age: int
    category: CategoryResponseSchema  # Nested CategoryModel
    rules: list[RuleResponseSchema]
