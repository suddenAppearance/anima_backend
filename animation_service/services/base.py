from fastapi import Depends
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.deps import get_session
from repositories.animations import AnimationsRepository


class BaseService:
    def __init__(self, request: Request, session: AsyncSession = Depends(get_session)):
        self.request = request
        self.session = session
        self._animations_repository: AnimationsRepository | None = None

    @property
    def animations_repository(self):
        self._animations_repository = self._animations_repository or AnimationsRepository(self.session)
        return self._animations_repository
