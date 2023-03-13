from uuid import UUID

from fastapi import UploadFile

from gateways.base import BaseAsyncGateway


class FileServiceGateway(BaseAsyncGateway):
    async def get_files(self, type: str):
        return await self._client.get(
            "/api/v1/files/", headers=self.clear_headers(self.request.headers), params={"type": type}
        )

    async def upload_file(self, file: UploadFile):
        return await self._client.put(
            "/api/v1/files/",
            headers=self.clear_headers(self.request.headers),
            files={"file": (file.filename, file.file)},
        )

    async def create_meta(self, json: dict):
        return await self._client.post("/api/v1/files/", headers=self.clear_headers(self.request.headers), json=json)

    async def animate(self, model_id: UUID, animation_id: UUID):
        return await self._client.post(
            f"/api/v1/models/{model_id}:animate/{animation_id}/", headers=self.clear_headers(self.request.headers)
        )
