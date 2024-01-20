from .controller import router
from ..schemas.password_schema import PasswordSchema
from ..services.password_service import password_service


@router.post("/password/", response_model=PasswordSchema)
async def post_password(string: PasswordSchema):
    password = string.password
    user = password_service(password)
    return f"Person added  with following id: {(user.id)}"