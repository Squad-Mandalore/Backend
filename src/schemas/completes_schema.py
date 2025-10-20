from datetime import date

from pydantic import BaseModel

from src.schemas.exercise_schema import ExerciseResponseSchema
from src.schemas.trainer_schema import TrainerResponseSchema


class CompletesPostSchema(BaseModel):
    exercise_id: str
    athlete_id: str
    result: str


class CompletesPatchSchema(BaseModel):
    result: str | None = None


class CompletesResponseSchema(BaseModel):
    athlete_id: str
    exercise: ExerciseResponseSchema
    tracked_at: date
    tracked_by: str
    trainer: TrainerResponseSchema
    result: str
    points: int
