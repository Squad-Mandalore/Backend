from typing import Optional
from pydantic import BaseModel


class CategoryPostSchema(BaseModel):
    title: str

class CategoryPatchSchema(BaseModel):
    title: Optional[str] = None

class CategoryResponseSchema(BaseModel):
    id: str
    title: str
