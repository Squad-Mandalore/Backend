from sqlalchemy.orm import Session

from src.models.models import Category, Exercise
from src.models.values import parse_values


def test_parsevalues(session: Session):
    parse_values(session)
    # check if all values are parsed
    assert session.query(Category).count() == 4
    assert session.query(Exercise).count() == 37 + 9
