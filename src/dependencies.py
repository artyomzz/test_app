from typing import AsyncGenerator

from httpx import AsyncClient

from src.database import async_session_maker


async def get_client():
    async with AsyncClient() as client:
        yield client


async def get_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session
