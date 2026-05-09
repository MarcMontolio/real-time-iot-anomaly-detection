from collections.abc import AsyncGenerator, Generator

import psycopg

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.deps import get_db
from app.core.config import settings
from app.main import app


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    test_engine = create_async_engine(settings.test_database_url, echo=False)

    TestingSessionLocal = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with TestingSessionLocal() as session:
        yield session

    await test_engine.dispose()
        

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
        
        
@pytest.fixture(autouse=True)
def clean_devices_table() -> Generator[None]:
    test_sync_url = settings.test_database_sync_url.replace("+psycopg", "")

    with psycopg.connect(test_sync_url) as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM devices;")
        conn.commit()

    yield