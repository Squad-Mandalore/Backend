from src.schemas.user_schema import UserPatchSchema
from src.schemas.user_schema import UserPostSchema
from src.schemas.user_schema import UserResponseSchema


class TrainerPostSchema(UserPostSchema):
    pass


class TrainerPatchSchema(UserPatchSchema):
    pass


class TrainerResponseSchema(UserResponseSchema):
    pass
