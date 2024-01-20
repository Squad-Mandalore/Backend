from ..main import app
from ..schemas import password_schema
from ..models import password_model
from ..services.password_service import password_service


@app.post("/password", response_model=password_schema)
def post_password(string: password_schema):
    password = password_model(content=string.content)
    password_service(password)
    return "password added"
