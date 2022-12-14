from fastapi import APIRouter, Depends
from fastapi.requests import Request

from api.api_v1.endpoints.token import router as token_router
from api.api_v1.endpoints.projects import router as projects_router
from api.api_v1.deps import auth_required
from schemas.base import User

router = APIRouter()


@router.get("/")
async def healthcheck():
    return {}


@router.get("/me/", response_model=User, dependencies=[Depends(auth_required)])
async def get_current_user(request: Request):
    return request.user


router.include_router(token_router, prefix="/auth", include_in_schema=False)
router.include_router(projects_router, prefix="/projects", tags=["projects"])
