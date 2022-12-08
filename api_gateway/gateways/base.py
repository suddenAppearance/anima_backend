import logging

import httpx
from fastapi.requests import Request
from httpx import AsyncClient

logger = logging.getLogger("api")


class BaseAsyncGateway:
    def __init__(self, request: Request, client: AsyncClient):
        self._client = client
        self.request = request

    @staticmethod
    def clear_params(params: dict) -> dict:
        return {k: v for k, v in params.items() if v}
