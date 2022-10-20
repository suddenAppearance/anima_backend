import logging

from keycloak import KeycloakOpenID, KeycloakGetError

from core.settings import Settings

keycloak = KeycloakOpenID(
    server_url=Settings().KEYCLOAK_URL,
    realm_name=Settings().KEYCLOAK_REALM,
    client_id='account-console'
)