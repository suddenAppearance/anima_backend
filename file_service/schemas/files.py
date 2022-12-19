from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class FileInfoRetrieveSchema(BaseModel):
    id: UUID
    author_id: UUID
    bucket_name: str
    minio_path: str
    initial_filename: str
    size: int
    pretty_size: str | None
    hash: str

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
