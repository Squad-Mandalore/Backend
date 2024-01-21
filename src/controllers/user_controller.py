from fastapi import APIRouter, HTTPException
from src.database.database_utils import get_all

from src.models.user_model import User
from src.schemas.user_schema import UserSchema
from src.services.user_service import check_password

router = APIRouter()


@router.get("/allUser")
async def get_all_entries():
    return get_all(User)


@router.post("/login")
async def post_login(string: UserSchema):
    id = string.id
    password = string.password
    result = check_password(id, password)

    if result:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password or user")
