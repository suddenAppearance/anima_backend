from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer = HTTPBearer()


async def get_token(authorization: HTTPAuthorizationCredentials = Security(bearer)) -> str:
    return authorization.credentials
