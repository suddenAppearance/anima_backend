import asyncio
import logging
from datetime import datetime, timedelta

from minio import Minio

from core import settings
from models import async_engine
from schemas.base import MinioBuckets

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


async def wait_minio():
    timeout = 30
    now = datetime.now()
    logger.info(f"Connecting to minio at {settings.MinioConfig().get_url()}...")
    connected = False
    minio = None
    while now + timedelta(seconds=timeout) > datetime.now() and not connected:
        try:
            minio = Minio(
                endpoint=settings.MinioConfig().get_url(),
                access_key=settings.MinioConfig().MINIO_ACCESS_KEY,
                secret_key=settings.MinioConfig().MINIO_SECRET_KEY,
                secure=settings.MinioConfig().MINIO_SECURE
            )
            connected = True
        except Exception:  # noqa
            logger.info("Attempt to connect to minio failed... Retrying")
            await asyncio.sleep(5)

    if not connected:
        logger.info("Connection to minio failed...")
        raise ConnectionError(settings.MinioConfig().get_url())
    if connected and minio:
        logger.info("Connected to minio...")
        for bucket in MinioBuckets:
            if not minio.bucket_exists(bucket.value):
                logger.info(f"Bucket `{bucket}` does not exist. Creating...")
                minio.make_bucket(bucket.value)
                logger.info(f"Bucket `{bucket}` was created...")
            else:
                logger.info(f"Bucket `{bucket}` exists. Skipping...")
