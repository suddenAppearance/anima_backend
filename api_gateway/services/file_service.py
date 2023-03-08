from fastapi import UploadFile

from schemas.files import FileMetaCreateSchema
from services.base import FileServiceMixin, FileServiceGatewayMixin


class FileService(FileServiceMixin, FileServiceGatewayMixin):
    async def get_files(self, type: str):
        return self.adapt_response(await self.file_service_gateway.get_files(type))

    async def upload_file(self, file: UploadFile):
        return self.adapt_response(await self.file_service_gateway.upload_file(file))

    async def create_meta(self, meta: FileMetaCreateSchema):
        return self.adapt_response(await self.file_service_gateway.create_meta(meta.dict()))
