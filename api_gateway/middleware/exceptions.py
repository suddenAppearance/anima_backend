import logging
import traceback
from json import JSONDecodeError
from typing import Callable, Awaitable, Type

import httpx
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse

logger = logging.getLogger("api")


async def exceptions_wrapper(request: Request, call_next: Callable[[Request], Awaitable]):
    try:
        return await call_next(request)
    except httpx.HTTPStatusError as e:
        try:
            json_data = e.response.json()
            return JSONResponse(
                json_data, e.response.status_code
            )
        except JSONDecodeError:
            return JSONResponse(
                {"data": e.response.content.decode()}, e.response.status_code
            )
    except Exception as exc:  # noqa
        logger.error(f"{exc.__class__.__name__}: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            {"message": f"{exc.__class__.__name__}: {exc}", "traceback": traceback.format_exception(exc)}, 500
        )
