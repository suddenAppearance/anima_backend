from gateways.base import BaseAsyncGateway


class AnimationServiceGateway(BaseAsyncGateway):
    async def get_animations_by_project_id(self, project_id: int):
        return await self._client.get(
            "/api/v1/animations/", params={"project_id": project_id}, headers=self.clear_headers(self.request.headers)
        )

    async def create_animation(self, json: dict):
        return await self._client.post(
            "/api/v1/animations/", json=json, headers=self.clear_headers(self.request.headers)
        )
