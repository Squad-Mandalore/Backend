from sqlalchemy.orm import Session
from src.models.models import Category, Exercise
from src.models.values import parse_values

from tests.define_test_variables import session_fixture

def test_parsevalues(session: Session):
    parse_values(session)
    # check if all values are parsed
    assert session.query(Category).count() == 4
    assert session.query(Exercise).count() == 37 + 9
