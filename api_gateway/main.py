import logging
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.api_v1.api import router as api_v1
from core import settings
from core.launch import wait_keycloak
from gateways.keycloak import keycloak_gateway
from middleware.authorization import KeycloakAuthenticationMiddleware, KeycloakAuthBackend
from middleware.exceptions import exceptions_wrapper
from services.base import project_service_client, animation_service_client, file_service_client

dictConfig(settings.LogConfig().config)

app = FastAPI(
    title="Anima API Gateway",
    description="API Gateway для сервисов Anima"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.AppConfig().CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.AppConfig().CORS_ALLOW_METHODS,
    allow_headers=settings.AppConfig().CORS_ALLOW_HEADERS,
)
app.add_middleware(KeycloakAuthenticationMiddleware, backend=KeycloakAuthBackend())
app.middleware("http")(exceptions_wrapper)


@app.on_event("startup")
async def on_startup(_=None):
    await wait_keycloak()


@app.on_event("shutdown")
async def on_shutdown(_=None):
    keycloak_gateway.close()
    await project_service_client.aclose()
    await animation_service_client.aclose()
    await file_service_client.aclose()


app.include_router(api_v1, prefix="/api/v1")
