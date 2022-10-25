import logging
import traceback
from urllib.parse import urlparse

import pkce
import urllib3
from fastapi import HTTPException
from keycloak import KeycloakOpenID, KeycloakGetError, KeycloakPostError

from core.settings import Settings

keycloak = KeycloakOpenID(
    server_url=Settings().KEYCLOAK_URL,
    realm_name=Settings().KEYCLOAK_REALM,
    client_id='account-console'
)


class UsersService:
    def get_login_page_and_code_verifier(self, redirect_url):
        code_verifier = pkce.generate_code_verifier(length=128)
        code_challenge = pkce.get_code_challenge(code_verifier)
        auth_endpoint = urlparse(keycloak.well_known()["authorization_endpoint"].replace("keycloak:8080", "localhost:8787")).geturl()
        return (
            f"{auth_endpoint}?"
            f"client_id=account-console&"
            f"response_type=code&"
            f"redirect_uri={redirect_url}&"
            f"scope=email&"
            f"code_challenge={code_challenge}&"
            f"code_challenge_method=S256"
        ), code_verifier

    async def get_token_by_code(self, code: str, redirect_url: str, code_verifier: str):
        try:
            access_token = keycloak.token(
                grant_type="authorization_code",
                code=code,
                redirect_uri=redirect_url,
                code_verifier=code_verifier,
                client_id="account-console",
            )
        except KeycloakPostError as e:
            logging.getLogger().info(f"Error occured:\n {e}\n {traceback.format_exc()}")
            raise HTTPException(status_code=404, detail={"message": "Not found"})

        return access_token  # почему-то не хочет подтверждаться
