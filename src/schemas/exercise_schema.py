from pydantic import BaseModel

from src.schemas.category_schema import CategoryResponseSchema
from src.schemas.rule_schema import RuleResponseSchema


class ExercisePostSchema(BaseModel):
    title: str
    category_id: str
    # rule_id: str


class ExercisePatchSchema(BaseModel):
    title: str | None = None


class ExerciseResponseSchema(BaseModel):
    id: str
    title: str
    category: CategoryResponseSchema  # Nested CategoryModel
    rules: list[RuleResponseSchema]
