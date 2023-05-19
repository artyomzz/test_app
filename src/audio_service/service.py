from uuid import UUID

from pydub import AudioSegment
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.audio_service.models import Record, User


async def create_user_in_db(username: str, session: AsyncSession):
    user = User(username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def save_record_to_db(
    user_id: str | UUID, access_token: str | UUID, content: bytes, session: AsyncSession
):
    record = Record(user_id=user_id, access_token=access_token, data=content)
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


def convert_to_mp3(wav_filename: str, mp3_filename: str):
    sound = AudioSegment.from_wav(wav_filename)
    sound.export(mp3_filename, format="mp3")


async def get_record_from_db(
    id: str | UUID, user_id: str | UUID, session: AsyncSession
):
    query_res = await session.execute(
        select(Record).where(and_(Record.id == id, Record.user_id == user_id))
    )
    return query_res.scalar()
