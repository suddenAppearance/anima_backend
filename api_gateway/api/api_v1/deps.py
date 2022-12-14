import logging

from fastapi import Security
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer

logger = logging.getLogger("api")

bearer = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token/")
http_bearer = HTTPBearer()


async def auth_required(
    authorization: HTTPAuthorizationCredentials = Security(bearer),
    http_authorization: HTTPAuthorizationCredentials = Security(http_bearer),
) -> None:
    pass
