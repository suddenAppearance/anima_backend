from typing import Tuple

import jwt
import pydantic
from fastapi.responses import JSONResponse
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from gateways.keycloak import keycloak_gateway
from schemas.base import User


class KeycloakAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, User | None]:
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, None
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise AuthenticationError("Not authenticated")
        if scheme.lower() != "bearer":
            raise AuthenticationError("Invalid authentication scheme")
        try:
            userinfo = keycloak_gateway.userinfo(token=credentials)
        except jwt.DecodeError:
            raise AuthenticationError(f"Invalid JWT token")
        try:
            user = User(**userinfo)
            return True, user
        except pydantic.ValidationError:
            raise AuthenticationError("Unsupported token format")


class KeycloakAuthenticationMiddleware(BaseAuthenticationMiddleware):
    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=403, content={"detail": str(exc)})
