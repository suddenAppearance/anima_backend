import hashlib
import os.path
from io import BytesIO
from uuid import UUID

from fastapi import UploadFile, HTTPException
from typing.io import BinaryIO

from models import File
from schemas.base import MinioBuckets
from schemas.files import FileInfoRetrieveSchema
from services.base import BaseService


class FileService(BaseService):
    @property
    def repository(self):
        return self.files_repository

    def get_minio_path(self, filename: str) -> str:
        return os.path.join(str(self.request.user.sub), filename)

    @staticmethod
    def get_hash_sum(file: BinaryIO) -> str:
        hasher = hashlib.md5()
        while chunk := file.read(8192):
            hasher.update(chunk)

        file.seek(0)
        return hasher.hexdigest()

    @staticmethod
    def get_file_size(file: BinaryIO) -> int:
        return os.fstat(file.fileno()).st_size

    def get_file_obj(self, file: UploadFile) -> File:
        file = File(
            author_id=self.request.user.sub,
            bucket_name=MinioBuckets.USERS_FILES,
            minio_path=self.get_minio_path(file.filename),
            initial_filename=file.filename,
            size=self.get_file_size(file.file),
            hash=self.get_hash_sum(file.file),
        )
        return file

    async def minio_upload_file(self, file: UploadFile):
        self.minio.put_object(
            bucket_name=MinioBuckets.USERS_FILES.value,
            object_name=self.get_minio_path(file.filename),
            data=BytesIO(await file.read()),
            length=self.get_file_size(file.file),
            content_type=file.content_type,
        )

    async def create(self, file: UploadFile) -> FileInfoRetrieveSchema:
        if await self.repository.get_by_filename_and_author_id(file.filename, self.request.user.sub):
            raise HTTPException(
                status_code=409, detail={"message": f"Current user already has file with name `{file.filename}`"}
            )
        file_obj = self.get_file_obj(file)
        await self.minio_upload_file(file)
        file_obj = await self.repository.create(file_obj)
        return FileInfoRetrieveSchema.from_orm(file_obj)

    async def get_all(self) -> list[FileInfoRetrieveSchema]:
        files = await self.repository.get_all()
        return [FileInfoRetrieveSchema.from_orm(file) for file in files]

    async def get_file_info_by_id(self, id: UUID):
        file = await self.repository.get_by_id(id)
        if not file:
            return None
        return FileInfoRetrieveSchema.from_orm(file)
