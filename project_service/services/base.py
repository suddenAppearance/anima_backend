import logging

from fastapi import Depends
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.deps import get_session
from repositories.projects import ProjectsRepository


class BaseService:
    def __init__(self, request: Request, session: AsyncSession = Depends(get_session)):
        self.request = request
        self.session = session
        self.logger = logging.getLogger("api")
        self._projects_repository: ProjectsRepository | None = None

    @property
    def projects_repository(self) -> ProjectsRepository:
        self._projects_repository = self._projects_repository or ProjectsRepository(self.session)
        return self._projects_repository
