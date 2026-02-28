from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from supabase_auth.errors import AuthApiError

from app.api.router import main_router
from app.core.config import settings
from app.core.exception import FridayNightException


app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AuthApiError)
async def supabase_auth_exception_handler(request: Request, exc: AuthApiError):
    return JSONResponse(
        status_code=400,
        content={"message": "Error de validação", "detail": exc.message},
    )


@app.exception_handler(FridayNightException)
async def friday_night_exception_handler(request: Request, exc: FridayNightException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "message": exc.message},
    )


app.include_router(main_router)

add_pagination(app)
