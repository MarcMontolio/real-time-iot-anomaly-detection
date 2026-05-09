from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings


async_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)