from src.controllers.controller import router
from src.schemas.user_schema import UserSchema
from src.services.user_service import check_password


@router.post("/login/", response_model=UserSchema)
async def post_login(string: UserSchema):
    id = string.id
    password = string.password
    result = check_password(id, password)
    return f"The password is {result}"
