from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from src.schemas.exercise_schema import ExerciseResponseSchema


class CompletesPostSchema(BaseModel):
    exercise_id: str
    athlete_id: str
    tracked_at: date
    result: str
    points: int

class CompletesPatchSchema(BaseModel):
    athlete_id: Optional[str]
    exercise_id: Optional[str]
    tracked_at: Optional[date]
    tracked_by: Optional[str]
    result: Optional[str]
    points: Optional[int]

class CompletesResponseSchema(BaseModel):
    athlete_id: str
    exercise: ExerciseResponseSchema
    tracked_at: date
    tracked_by: str
    result: str
    points: int
