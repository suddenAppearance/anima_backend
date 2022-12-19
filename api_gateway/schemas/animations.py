from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, constr

from schemas.base import UserInfo


class AnimationCreateSchema(BaseModel):
    title: constr(max_length=55)
    project_id: int
    file_id: UUID


class AnimationAuthor(UserInfo):
    pass


class AnimationRetrieveSchema(AnimationCreateSchema):
    id: int
    author_id: UUID
    author: AnimationAuthor

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
