from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, AnyUrl


class FileInfoRetrieveSchema(BaseModel):
    id: UUID
    author_id: UUID
    bucket_name: str
    minio_path: str
    initial_filename: str
    size: int
    pretty_size: str | None
    hash: str
    download_url: AnyUrl | None

    created_at: datetime


class FileMetaTypeEnum(str, Enum):
    CHARACTER = "CHARACTER"
    ANIMATION = "ANIMATION"


class FileMetaCreateSchema(BaseModel):
    file_id: UUID
    title: str
    type: FileMetaTypeEnum


class FileMetaRetrieveSchema(BaseModel):
    file_id: UUID
    title: str
    type: FileMetaTypeEnum

    file: FileInfoRetrieveSchema
