import logging
from typing import Any
from uuid import UUID

from core import settings
from keycloak import KeycloakOpenID, KeycloakAdmin

logger = logging.getLogger("api")


class KeycloakGateway:
    def __init__(self, host: str, realm: str, email: str, password: str):
        self.host = host
        self.realm = realm
        self.email = email
        self.password = password
        self.client: KeycloakOpenID | None = None
        self.admin: KeycloakAdmin | None = None

    def open(self):
        self.client = KeycloakOpenID(
            server_url=self.host, realm_name=self.realm, client_id='account-console'
        )
        self.admin = KeycloakAdmin(
            server_url=self.host, realm_name=self.realm, username=self.email, password=self.password
        )

    def close(self):
        if self.client:
            self.client.connection._s.close()

    def userinfo(self, token) -> dict[str, Any]:
        return self.client.userinfo(token=token)

    def get_user_by_sub(self, sub: UUID) -> dict[str, Any]:
        return self.admin.get_user(user_id=str(sub))

    def login(self, username: str, password: str) -> dict:
        return self.client.token(username, password)


keycloak_gateway = KeycloakGateway(
    host=settings.KeycloakSettings().KEYCLOAK_HOST,
    realm=settings.KeycloakSettings().KEYCLOAK_REALM,
    email=settings.KeycloakSettings().KEYCLOAK_ADMIN_EMAIL,
    password=settings.KeycloakSettings().KEYCLOAK_ADMIN_PASSWORD,
)
