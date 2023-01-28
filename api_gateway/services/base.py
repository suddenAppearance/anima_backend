import logging

from fastapi.requests import Request


class BaseService:
    def __init__(self, request: Request):
        self.request = request
        self.logger = logging.getLogger("api")
