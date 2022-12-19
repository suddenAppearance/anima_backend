from uuid import UUID

from fastapi import UploadFile

from core import settings
from gateways.base import BaseAsyncGateway


class FileServiceGateway(BaseAsyncGateway):
    async def get_file_by_id(self, id: UUID):
        return await self._client.get(f"/api/v1/files/{id}/", headers=self.clear_headers(self.request.headers))

    async def get_all(self):
        return await self._client.get(f"/api/v1/files/", headers=self.clear_headers(self.request.headers))

    async def upload_file(self, file: UploadFile):
        return await self._client.put(
            f"/api/v1/files/",
            headers=self.clear_headers(self.request.headers),
            files={
                "file": (
                    file.filename,
                    file.file,
                    file.content_type
                )
            },
        )
