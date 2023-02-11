import logging

from fastapi import Depends
from fastapi.requests import Request
from fastapi.responses import Response
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.deps import get_session
from core import settings
from repositories.files import FilesRepository


class BaseService:
    def __init__(self, request: Request, session: AsyncSession = Depends(get_session)):
        self.request = request
        self.session = session
        self.logger = logging.getLogger("api")
        self._minio: Minio | None = None
        self._files_repository: FilesRepository | None = None

    @property
    def minio(self):
        self._minio = self._minio or Minio(
            endpoint=settings.MinioConfig().get_url(),
            access_key=settings.MinioConfig().MINIO_ACCESS_KEY,
            secret_key=settings.MinioConfig().MINIO_SECRET_KEY,
            secure=settings.MinioConfig().MINIO_SECURE
        )
        return self._minio

    @property
    def files_repository(self):
        self._files_repository = self._files_repository or FilesRepository(self.session)
        return self._files_repository

