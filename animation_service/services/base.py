from fastapi import Depends
from fastapi.requests import Request
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.deps import get_session
from core import settings


class BaseService:
    def __init__(self, request: Request, session: AsyncSession = Depends(get_session)):
        self.request = request
        self.session = session
