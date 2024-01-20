from ..main import app
from ..database.database_utils import get_all


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/all")
def get_all_entries():
    return get_all()
