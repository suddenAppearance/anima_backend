import asyncio
import logging
from datetime import datetime, timedelta

from core import settings
from models import async_engine

logger = logging.getLogger("api")


async def wait_database():
    timeout = 30
    now = datetime.now()
    logger.info(f"Connecting to database at {settings.DatabaseSettings().get_async_url()}...")
    connected = False
    while now + timedelta(seconds=timeout) > datetime.now() and not connected:
        try:
            await async_engine.connect()
            connected = True
        except Exception:  # noqa
            logger.info("Attempt to connect to database failed... Retrying")
            await asyncio.sleep(5)

    if not connected:
        logger.info("Connection to database failed...")
        raise ConnectionError(settings.DatabaseSettings().get_async_url())

    if connected:
        logger.info("Connected to database...")
