from httpx import Response

from gateways.base import BaseAsyncGateway


class ProjectServiceGateway(BaseAsyncGateway):
    async def create(self, json: dict) -> Response:
        return await self._client.post("/api/v1/projects/", json=json, headers=self.clear_headers(self.request.headers))

    async def get_projects(self) -> Response:
        return await self._client.get("/api/v1/projects/", headers=self.clear_headers(self.request.headers))

    async def get_project_by_id(self, id: int) -> Response:
        return await self._client.get(f"/api/v1/projects/{id}/", headers=self.clear_headers(self.request.headers))
