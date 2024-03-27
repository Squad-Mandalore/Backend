from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.schemas.exercise_schema import ExerciseResponseSchema


class CompletesPostSchema(BaseModel):
    athlete_id: str
    exercise_id: str
    tracked_at: datetime
    result: str
    points: int
    dbs: bool

class CompletesPatchSchema(BaseModel):
    athlete_id: Optional[str]
    exercise_id: Optional[str]
    tracked_at: Optional[datetime]
    completed_at: Optional[datetime]
    result: Optional[str]
    points: Optional[int]
    dbs: Optional[bool]

class CompletesResponseSchema(BaseModel):
    athlete_id: str
    exercise_id: ExerciseResponseSchema
    tracked_at: datetime
    completed_at: Optional[datetime]
    result: str
    points: int
    dbs: bool
