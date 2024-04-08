from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from src.schemas.exercise_schema import ExerciseResponseSchema
from src.schemas.trainer_schema import TrainerResponseSchema


class CompletesPostSchema(BaseModel):
    exercise_id: str
    athlete_id: str
    result: str
    points: int

class CompletesPatchSchema(BaseModel):
    result: Optional[str] = None
    points: Optional[int] = None

class CompletesResponseSchema(BaseModel):
    athlete_id: str
    exercise: ExerciseResponseSchema
    tracked_at: date
    tracked_by: str
    trainer: TrainerResponseSchema
    result: str
    points: int
