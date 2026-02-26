from fastapi import APIRouter


from app.modules.finance.categories.router import router as router_categories
from app.modules.finance.subcategories.router import router as router_subcategories
from app.modules.finance.tags.router import router as router_tag

finance_router = APIRouter(prefix="/finance", tags=["finance"])


finance_router.include_router(router_categories)
finance_router.include_router(router_subcategories)
finance_router.include_router(router_tag)
