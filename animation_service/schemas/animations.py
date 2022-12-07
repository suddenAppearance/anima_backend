from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, constr


class AnimationCreateSchema(BaseModel):
    title: constr(max_length=55)
    project_id: int
    file_id: UUID


class AnimationRetrieveSchema(AnimationCreateSchema):
    id: int

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
