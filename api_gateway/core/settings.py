from httpx import AsyncClient
from pydantic import BaseSettings, AnyUrl
from urllib3.util import Url


class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    def get_async_url(self) -> str:
        return str(
            Url(
                scheme="postgresql+asyncpg",
                auth=":".join((self.POSTGRES_USER, self.POSTGRES_PASSWORD)),
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB
            )
        )

    def get_sync_url(self):
        return str(
            Url(
                scheme="postgresql",
                auth=":".join((self.POSTGRES_USER, self.POSTGRES_PASSWORD)),
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB
            )
        )


class KeycloakSettings(BaseSettings):
    KEYCLOAK_HOST: str
    KEYCLOAK_REALM: str
    KEYCLOAK_ADMIN_EMAIL: str
    KEYCLOAK_ADMIN_PASSWORD: str


class LogConfig(BaseSettings):
    config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(asctime)s :: %(client_addr)s - "%(request_line)s" %(status_code)s',
                "use_colors": True,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "api": {"handlers": ["default"], "level": "DEBUG"},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        },
    }


class AppConfig(BaseSettings):
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]


class GatewaySettings(BaseSettings):
    PROJECT_SERVICE_GATEWAY: AnyUrl
    ANIMATION_SERVICE_GATEWAY: AnyUrl
    FILE_SERVICE_GATEWAY: AnyUrl
