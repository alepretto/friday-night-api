from fastapi import FastAPI

from app.api.router import main_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")


app.include_router(main_router)
