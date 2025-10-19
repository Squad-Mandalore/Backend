from src.schemas.trainer_schema import TrainerPatchSchema
from src.schemas.trainer_schema import TrainerPostSchema
from src.schemas.trainer_schema import TrainerResponseSchema


class AdminPostSchema(TrainerPostSchema):
    pass


class AdminPatchSchema(TrainerPatchSchema):
    pass


class AdminResponseSchema(TrainerResponseSchema):
    pass
