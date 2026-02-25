from fastapi import APIRouter


from app.modules.finance.categories.router import router as router_categories


finance_router = APIRouter(prefix="/finance", tags=["finance"])


finance_router.include_router(router_categories)
