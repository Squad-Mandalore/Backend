from src.schemas.user_schema import UserPatchSchema, UserPostSchema, UserResponseSchema

class AdminPostSchema(UserPostSchema):
    pass

class AdminPatchSchema(UserPatchSchema):
    pass

class AdminResponseSchema(UserResponseSchema):
    pass
