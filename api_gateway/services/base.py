import logging

from fastapi.requests import Request
from httpx import AsyncClient

from core import settings
from gateways.animation_service import AnimationServiceGateway
from gateways.file_service import FileServiceGateway
from gateways.keycloak import keycloak_gateway, KeycloakGateway
from gateways.project_service import ProjectServiceGateway

project_service_client = AsyncClient(base_url=settings.GatewaySettings().PROJECT_SERVICE_GATEWAY)
animation_service_client = AsyncClient(base_url=settings.GatewaySettings().ANIMATION_SERVICE_GATEWAY)
file_service_client = AsyncClient(base_url=settings.GatewaySettings().FILE_SERVICE_GATEWAY)


class BaseService:
    def __init__(self, request: Request):
        self.request = request
        self.logger = logging.getLogger("api")
        self._project_service_gateway: ProjectServiceGateway | None = None
        self._animation_service_gateway: AnimationServiceGateway | None = None
        self._file_service_gateway: FileServiceGateway | None = None
        self._keycloak: KeycloakGateway | None = None

    @property
    def animation_service_gateway(self):
        self._animation_service_gateway = self._animation_service_gateway or AnimationServiceGateway(
            self.request, animation_service_client
        )
        return self._animation_service_gateway

    @property
    def project_service_gateway(self):
        self._project_service_gateway = self._project_service_gateway or ProjectServiceGateway(
            self.request, project_service_client
        )
        return self._project_service_gateway

    @property
    def file_service_gateway(self):
        self._file_service_gateway = self._file_service_gateway or FileServiceGateway(
            self.request, file_service_client
        )
        return self._file_service_gateway

    @property
    def keycloak(self):
        self._keycloak = self._keycloak or keycloak_gateway
        self._keycloak.admin.get_token()
        return self._keycloak
