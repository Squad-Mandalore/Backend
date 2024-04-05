from http.client import HTTPException
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Base, Certificate
from src.services import update_service


