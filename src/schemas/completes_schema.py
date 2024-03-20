from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: str
    title: str

class ExerciseSchema(BaseModel):
    id: str
    title: str
    category: CategorySchema  # Nested CategoryModel
    from_age: int
    to_age: int

class CompletesSchema(BaseModel):
    athlete_id: str
    exercise_id: ExerciseSchema
    tracked_at: datetime
    completed_at: Optional[datetime]
    result: str
    points: int
    dbs: bool
