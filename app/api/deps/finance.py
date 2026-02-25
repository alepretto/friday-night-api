from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.core import get_db

from app.modules.finance.categories.repo import CategoryRepo
from app.modules.finance.categories.service import CategoryService


def get_category_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = CategoryRepo(db)
    return CategoryService(repo)


def get_subcategory_service(db: Annotated[AsyncSession, Depends(get_db)]):
    pass


def get_tag_service(db: Annotated[AsyncSession, Depends(get_db)]):
    pass
