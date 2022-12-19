from fastapi import APIRouter, UploadFile, Depends

from services.files import FilesService

router = APIRouter()


@router.put("/")
async def upload_file(file: UploadFile, file_service: FilesService = Depends()):
    return await file_service.upload_file(file)


@router.get("/")
async def get_all_files(file_service: FilesService = Depends()):
    return await file_service.get_all()
