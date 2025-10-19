from src.schemas.trainer_schema import (
    TrainerPatchSchema,
    TrainerPostSchema,
    TrainerResponseSchema,
)


class AdminPostSchema(TrainerPostSchema):
    pass


class AdminPatchSchema(TrainerPatchSchema):
    pass


class AdminResponseSchema(TrainerResponseSchema):
    pass
