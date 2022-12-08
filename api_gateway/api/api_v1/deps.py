import logging

from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger("api")

bearer = HTTPBearer()


async def auth_required(authorization: HTTPAuthorizationCredentials = Security(bearer)) -> None:
    pass
