from logging import Logger

import httpx
from fastapi import HTTPException, Depends
from fastapi.requests import Request
from httpx import AsyncClient

from api.api_v1.deps import get_logger
from core import settings
from gateways.file_service import FileServiceGateway

file_service_gateway_client = AsyncClient(base_url=settings.GatewaySettings().FILE_SERVICE_GATEWAY)


class BaseService:
    def __init__(self, request: Request, logger: Logger = Depends(get_logger)):
        self.request = request
        self.logger = logger

    @staticmethod
    def adapt_response(response: httpx.Response, expected_statuses=range(200, 300)) -> dict | list | str:
        body = response.json() if response.headers.get("content-type") == "application/json" else response.text
        if response.status_code not in expected_statuses:
            raise HTTPException(
                status_code=response.status_code,
                detail=body,
            )

        return body


class FileServiceMixin(BaseService):
    @property
    def file_service(self):
        from services.file_service import FileService

        # singleton per request
        if not hasattr(self.request, "_file_service"):
            setattr(self.request, "_file_service", FileService(self.request, self.logger))
        service: FileService = getattr(self.request, "_file_service")

        return service


class FileServiceGatewayMixin(BaseService):
    @property
    def file_service_gateway(self):
        if not hasattr(self.request, "_file_service_gateway"):
            setattr(
                self.request, "_file_service_gateway", FileServiceGateway(self.request, file_service_gateway_client)
            )

        gateway: FileServiceGateway = getattr(self.request, "_file_service_gateway")
        return gateway
