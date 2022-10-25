from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from api.api_v1.deps import get_token
from services.users import UsersService

router = APIRouter()

# @router.get("/")
# async def get_current_user(token: str = Depends(get_token)):
#     return UsersService().get_user_by_token(token)
code_verifier = None


@router.get("/")
async def redirect_to_login_page(request: Request):
    global code_verifier
    url, code_verifier = UsersService().get_login_page_and_code_verifier("http://0.0.0.0:8000/api/v1/users/redirect/")
    return RedirectResponse(url)


@router.get("/login/")
async def get_login_url(redirect_url: str):
    return UsersService().get_login_page_and_code_verifier(redirect_url)


@router.get("/callback/")
async def get_token(redirect_url: str, code: str, code_verifier: str):
    return await UsersService().get_token_by_code(code=code, code_verifier=code_verifier, redirect_url=redirect_url)


@router.get('/redirect/')
async def get_code(request: Request, code: str):
    return await UsersService().get_token_by_code(redirect_url="http://0.0.0.0:8000/api/v1/users/redirect/",
                                                  code_verifier=code_verifier, code=code)
