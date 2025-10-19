from src.schemas.user_schema import UserPatchSchema, UserPostSchema, UserResponseSchema


class TrainerPostSchema(UserPostSchema):
    pass


class TrainerPatchSchema(UserPatchSchema):
    pass


class TrainerResponseSchema(UserResponseSchema):
    pass
