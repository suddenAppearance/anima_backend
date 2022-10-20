from fastapi import APIRouter, Depends

from api.api_v1.deps import get_token
from services.users import UsersService

router = APIRouter()


@router.get("/")
async def get_current_user(token: str = Depends(get_token)):
    return UsersService().get_user_by_token(token)
