import logging

from fastapi import Depends
from fastapi.requests import Request
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.deps import get_session
from core import settings
from repositories.files import FilesRepository, FileMetaRepository, CompiledAnimationRepository

minio_service = Minio(
    endpoint=settings.MinioConfig().get_url(),
    access_key=settings.MinioConfig().MINIO_ACCESS_KEY,
    secret_key=settings.MinioConfig().MINIO_SECRET_KEY,
    secure=settings.MinioConfig().MINIO_SECURE,
)


class BaseService:
    def __init__(self, request: Request, session: AsyncSession = Depends(get_session)):
        self.request = request
        self.session = session
        self.logger = logging.getLogger("api")


class MinioMixin(BaseService):
    @property
    def minio(self):
        if not hasattr(self.request, "_minio"):
            setattr(
                self.request,
                "_minio",
                minio_service,
            )
        minio: Minio = getattr(self.request, "_minio")
        return minio


class FileServiceMixin(BaseService):
    @property
    def file_service(self):
        from services.files import FileService

        if not hasattr(self.request, "_file_service"):
            setattr(self.request, "_file_service", FileService(self.request, self.session))
        file_service: FileService = getattr(self.request, "_file_service")

        return file_service

    @property
    def file_repository(self):
        if not hasattr(self.request, "_file_repository"):
            setattr(self.request, "_file_repository", FilesRepository(self.session))
        file_repository: FilesRepository = getattr(self.request, "_file_repository")

        return file_repository


class FileMetaServiceMixin(BaseService):
    @property
    def file_meta_service(self):
        from services.files import FileMetaService

        if not hasattr(self.request, "_file_meta_service"):
            setattr(self.request, "_file_meta_service", FileMetaService(self.request, self.session))
        file_meta_service: FileMetaService = getattr(self.request, "_file_meta_service")

        return file_meta_service

    @property
    def file_meta_repository(self):

        if not hasattr(self.request, "_file_meta_repository"):
            setattr(self.request, "_file_meta_repository", FileMetaRepository(self.session))
        file_meta_repository: FileMetaRepository = getattr(self.request, "_file_meta_repository")

        return file_meta_repository


class AnimationServiceMixin(BaseService):
    @property
    def animation_service(self):
        from services.characters import AnimationService

        if not hasattr(self.request, "_animation_service"):
            setattr(self.request, "_animation_service", AnimationService(self.request, self.session))

        animation_service: AnimationService = getattr(self.request, "_animation_service")
        return animation_service


class CompiledAnimationServiceMixin(BaseService):
    @property
    def compiled_animation_service(self):
        from services.files import CompiledAnimationService

        if not hasattr(self.request, "_compiled_animation_service"):
            setattr(self.request, "_compiled_animation_service", CompiledAnimationService(self.request, self.session))

        compiled_animation_service: CompiledAnimationService = getattr(self.request, "_compiled_animation_service")
        return compiled_animation_service

    @property
    def compiled_animation_repository(self):
        if not hasattr(self.request, "_compiled_animation_repository"):
            setattr(self.request, "_compiled_animation_repository", CompiledAnimationRepository(self.session))

        compiled_animation_repository: CompiledAnimationRepository = getattr(
            self.request, "_compiled_animation_repository"
        )
        return compiled_animation_repository
