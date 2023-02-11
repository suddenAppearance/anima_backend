from gateways.base import BaseAsyncGateway


class FileServiceGateway(BaseAsyncGateway):
    async def get_files(self):
        return await self._client.get("/api/v1/files/", headers=self.clear_headers(self.request.headers))
