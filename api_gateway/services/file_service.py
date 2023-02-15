from services.base import FileServiceMixin, FileServiceGatewayMixin


class FileService(FileServiceMixin, FileServiceGatewayMixin):
    async def get_files(self, type: str):
        return self.adapt_response(await self.file_service_gateway.get_files(type))