from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from schemas.base import UserInfo


class FileAuthor(UserInfo):
    pass


class FileInfoRetrieveSchema(BaseModel):
    id: UUID
    author_id: UUID
    bucket_name: str
    minio_path: str
    initial_filename: str
    size: int
    pretty_size: str
    hash: str

    author: FileAuthor

    created_at: datetime

    class Config:
        orm_mode = True
