from fastapi import FastAPI
from api.api_v1.api import router as api_v1

app = FastAPI()



app.include_router(api_v1, prefix="/api/v1")