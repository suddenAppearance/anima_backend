import logging
from asyncio import shield
from typing import AsyncGenerator

from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from models import create_async_session

logger = logging.getLogger("api")

bearer = HTTPBearer()


async def auth_required(authorization: HTTPAuthorizationCredentials = Security(bearer)) -> None:
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = create_async_session()
    try:
        yield session
        try:
            await session.commit()
            logger.info("Transaction has been commited...")
        except DBAPIError:
            await session.rollback()
            logger.info("Transaction has been rolled back...")
    except Exception:
        await session.rollback()
        logger.info("Transaction has been rolled back...")
        raise
    finally:
        if session:
            await shield(session.close())
            await session.close()
            logger.info("Closed session...")
