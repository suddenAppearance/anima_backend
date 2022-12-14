import logging

from fastapi.datastructures import Headers
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

    @staticmethod
    def clear_headers(headers: dict | Headers) -> dict:
        not_allowed_headers = ('content-length',)
        headers = dict(headers)
        return {k: v for k, v in headers.items() if k.lower() not in not_allowed_headers}
