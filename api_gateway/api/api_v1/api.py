from fastapi import APIRouter, Depends
from fastapi.requests import Request

from api.api_v1.deps import auth_required
from schemas.base import User

router = APIRouter()


@router.get("/")
async def healthcheck():
    return {}


@router.get("/me/", response_model=User, dependencies=[Depends(auth_required)])
async def get_current_user(request: Request):
    return request.user
