from fastapi import APIRouter, Depends, Query

from api.api_v1.deps import auth_required
from services.file_service import FileService

router = APIRouter()


@router.get("/", dependencies=[Depends(auth_required)])
async def get_files(service: FileService = Depends(), type: str = Query(...)):
    return await service.get_files(type)
