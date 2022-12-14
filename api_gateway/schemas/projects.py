from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, constr

from schemas.base import UserInfo


class ProjectCreateSchema(BaseModel):
    title: constr(max_length=55)
    description: constr(max_length=240)


class ProjectAuthor(UserInfo):
    pass


class ProjectRetrieveSchema(ProjectCreateSchema):
    id: int
    author_id: UUID
    author: ProjectAuthor

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
