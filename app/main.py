from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from supabase_auth.errors import AuthApiError

from app.api.router import main_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")


@app.exception_handler(AuthApiError)
async def supabase_auth_exception_handler(request: Request, exc: AuthApiError):
    return JSONResponse(
        status_code=400,
        content={"message": "Error de validação", "detail": exc.message},
    )


app.include_router(main_router)
