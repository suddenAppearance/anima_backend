from asyncio import shield
from typing import AsyncGenerator

from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from models import create_async_session

bearer = HTTPBearer()


async def auth_required(authorization: HTTPAuthorizationCredentials = Security(bearer)) -> None:
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = create_async_session()
    try:
        yield session
    finally:
        if session:
            try:
                await session.commit()
            except DBAPIError:
                await session.rollback()
            await shield(session.close())
            await session.close()
