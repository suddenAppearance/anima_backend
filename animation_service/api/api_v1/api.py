from fastapi import APIRouter, Depends
from fastapi.requests import Request

from api.api_v1.deps import auth_required
from api.api_v1.endpoints.animation import router as animation_router
from models import create_async_session, create_session
from schemas.base import User

router = APIRouter()


@router.get("/")
async def healthcheck():
    async with create_async_session() as async_session:
        with create_session() as sync_session:
            sync_query = None
            async_query = None
            try:
                sync_query = sync_session.execute("SELECT 1") is not None
                async_query = await async_session.execute("SELECT 1") is not None
            except Exception:
                pass

            return {"asyncpg_connection": async_query, "psycopg2_connection": sync_query, "animation_service": True}


@router.get("/me/", response_model=User, dependencies=[Depends(auth_required)])
async def get_current_user(request: Request):
    return request.user


router.include_router(animation_router, prefix="/animations", tags=["animations"])
