from datetime import date
from typing import Optional
from pydantic import BaseModel

from src.models.models import Gender

class RulePostSchema(BaseModel):
    gender: Gender
    from_age: int
    to_age: int
    bronze: str
    silver: str
    gold: str
    year: date

class RulePatchSchema(BaseModel):
    gender: Optional[Gender]
    from_age: Optional[int]
    to_age: Optional[int]
    bronze: Optional[str]
    silver: Optional[str]
    gold: Optional[str]
    year: Optional[date]

class RuleResponseSchema(BaseModel):
    id: str
    gender: Gender
    from_age: int
    to_age: int
    bronze: str
    silver: str
    gold: str
    year: date
