from fastapi import APIRouter
from fastapi.responses import Response

from api.api_v1.endpoints.users import router as users_router

router = APIRouter()


@router.get("/")
async def healthcheck():
    return Response(status_code=200)


router.include_router(users_router, prefix="/users")
