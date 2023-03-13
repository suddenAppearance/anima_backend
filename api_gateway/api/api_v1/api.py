from fastapi import APIRouter, Depends
from fastapi.requests import Request

from api.api_v1.deps import auth_required
from api.api_v1.endpoints.characters import router as characters_router
from api.api_v1.endpoints.files import router as files_router
from api.api_v1.endpoints.token import router as token_router
from schemas.base import User

router = APIRouter()


@router.get("/")
async def healthcheck():
    return {}


@router.get("/me/", response_model=User, dependencies=[Depends(auth_required)])
async def get_current_user(request: Request):
    return request.user


router.include_router(token_router, prefix="/auth", include_in_schema=False)
router.include_router(files_router, prefix="/files", tags=["files"])
router.include_router(characters_router, prefix="/models", tags=["models"])
