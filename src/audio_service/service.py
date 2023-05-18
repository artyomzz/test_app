from sqlalchemy.ext.asyncio import AsyncSession

from src.audio_service.models import User


async def create_user_in_db(username: str, session: AsyncSession):
    user = User(username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
