from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.api_v1.api import router as api_v1
from core import settings
from core.launch import wait_database, wait_minio
from middleware.authorization import KeycloakAuthenticationMiddleware, KeycloakAuthBackend
from middleware.exceptions import exceptions_wrapper

dictConfig(settings.LogConfig().config)

app = FastAPI(
    title="File Service Anima API",
    description="Сервис работы с файлами"
)

# Middleware
app.add_middleware(KeycloakAuthenticationMiddleware, backend=KeycloakAuthBackend())
app.middleware("http")(exceptions_wrapper)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.AppConfig().CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.AppConfig().CORS_ALLOW_METHODS,
    allow_headers=settings.AppConfig().CORS_ALLOW_HEADERS,
)


@app.on_event("startup")
async def on_startup(_=None):
    await wait_database()
    await wait_minio()


app.include_router(api_v1, prefix="/api/v1")
