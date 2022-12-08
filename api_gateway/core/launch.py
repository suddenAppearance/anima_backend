import asyncio
import logging
from datetime import datetime, timedelta

from keycloak import KeycloakError

from core import settings
from gateways.keycloak import keycloak_gateway

logger = logging.getLogger("api")


async def wait_keycloak():
    timeout = 30
    now = datetime.now()
    logger.info(f"Connecting to keycloak at {settings.KeycloakSettings().KEYCLOAK_HOST}...")
    connected = False
    while now + timedelta(seconds=timeout) > datetime.now() and not connected:
        try:
            keycloak_gateway.open()
            connected = True
        except KeycloakError as e:
            logger.info(f"Connection to keycloak failed. Retrying...")
            logger.info(e)
            await asyncio.sleep(5)
    if not connected:
        logger.info("Connection to keycloak failed...")
        raise ConnectionError(settings.KeycloakSettings().KEYCLOAK_HOST)

    if connected:
        logger.info("Connected to keycloak...")
