from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    connect_args={"prepared_statement_cache_size": 0, "statement_cache_size": 0},
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, autocommit=False, autoflush=False
)
