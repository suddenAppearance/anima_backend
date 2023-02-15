from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, validator, AnyUrl


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

    class Config:
        orm_mode = True

    @validator("pretty_size")
    def prettify_size(cls, value: str | None, values: dict[str, ...]) -> str:
        size: int = values["size"]
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if abs(size) < 1024:
                return f"{size:3.1f} {unit}B"
            size /= 1024
        return f"{size:.1f} YB"


class FileMetaTypeEnum(str, Enum):
    CHARACTER = "CHARACTER"
    ANIMATION = "ANIMATION"


class FileMetaRetrieveSchema(BaseModel):
    file_id: UUID
    title: str
    type: FileMetaTypeEnum

    file: FileInfoRetrieveSchema

    class Config:
        orm_mode = True
