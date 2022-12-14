from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from gateways.keycloak import keycloak_gateway

router = APIRouter()


@router.post("/token/")
async def get_token(creds: OAuth2PasswordRequestForm = Depends()):
    return keycloak_gateway.login(creds.username, creds.password)
