import hashlib
import os.path
from io import BytesIO
from urllib.parse import urlparse
from uuid import UUID

from fastapi import UploadFile, HTTPException
from typing.io import BinaryIO

from core import settings
from models import File, FileMeta
from repositories.files import FileMetaRepository
from schemas.base import MinioBuckets
from schemas.files import FileInfoRetrieveSchema, FileMetaRetrieveSchema, FileMetaTypeEnum, FileMetaCreateSchema
from services.base import FileServiceMixin, MinioMixin, FileMetaServiceMixin


class FileService(FileServiceMixin, MinioMixin):
    @property
    def repository(self):
        return self.file_repository

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
        return File(
            author_id=self.request.user.sub,
            bucket_name=MinioBuckets.USERS_FILES,
            minio_path=self.get_minio_path(file.filename),
            initial_filename=file.filename,
            size=self.get_file_size(file.file),
            hash=self.get_hash_sum(file.file),
        )

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
        files = [FileInfoRetrieveSchema.from_orm(file) for file in files]
        for file in files:
            file.download_url = await self.get_presigned_url(file)
        return files

    async def get_presigned_url(self, file: File | FileInfoRetrieveSchema):
        url = urlparse(
            self.minio.get_presigned_url(
                method="GET",
                bucket_name=MinioBuckets.USERS_FILES,
                object_name=self.get_minio_path(file.initial_filename),
            )
        )
        return url._replace(netloc=settings.MinioConfig().MINIO_PROXY_HOST).geturl()

    async def get_file_info_by_id(self, id: UUID):
        file_obj = await self.repository.get_by_id(id)
        if not file_obj:
            return None

        file_obj = FileInfoRetrieveSchema.from_orm(file_obj)
        file_obj.download_url = await self.get_presigned_url(file_obj)
        return file_obj


class FileMetaService(FileMetaServiceMixin, FileServiceMixin):
    @property
    def repository(self) -> FileMetaRepository:
        return self.file_meta_repository

    async def create(self, meta: FileMetaCreateSchema) -> FileMetaRetrieveSchema:
        file_obj = await self.file_service.get_file_info_by_id(meta.file_id)
        if not file_obj:
            raise HTTPException(status_code=404, detail="Not found")

        await self.repository.create(FileMeta(**meta.dict()))
        return await self.get_full_file(meta.file_id)

    async def get_full_file(self, file_id: UUID) -> FileMetaRetrieveSchema:
        full_file = await self.repository.get_by_file_id(file_id, load_file=True)
        return FileMetaRetrieveSchema.from_orm(full_file) if full_file else None

    async def get_full_by_type(self, type: FileMetaTypeEnum) -> list[FileMetaRetrieveSchema]:
        full_files = await self.repository.get_by_type(type, load_file=True)
        full_files = [FileMetaRetrieveSchema.from_orm(file) for file in full_files]
        for full_file in full_files:
            full_file.file.download_url = await self.file_service.get_presigned_url(full_file.file)

        return full_files
