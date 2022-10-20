from pydantic import BaseSettings


class Settings(BaseSettings):
    KEYCLOAK_REALM: str
    KEYCLOAK_URL: str
