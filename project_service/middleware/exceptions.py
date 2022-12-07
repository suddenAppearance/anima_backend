import logging
import traceback
from typing import Callable, Awaitable, Type

from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse

logger = logging.getLogger("api")


async def exceptions_wrapper(request: Request, call_next: Callable[[Request], Awaitable]):
    try:
        return await call_next(request)
    except Exception as exc:  # noqa
        logger.error(f"{exc.__class__.__name__}: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            {"message": f"{exc.__class__.__name__}: {exc}", "traceback": traceback.format_exception(exc)}, 500
        )
