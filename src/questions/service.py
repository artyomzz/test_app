from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import QUESTIONS_URL
from src.questions.models import Question as QuestionModel
from src.questions.schemas import Question


async def fetch_questions(
    client: AsyncClient,
    questions_num: int,
) -> list[Question]:
    resp = await client.get(QUESTIONS_URL.format(questions_num))
    resp.raise_for_status()
    resp_json = resp.json()
    return [Question(**item) for item in resp_json]


async def save_questions_to_db(
        session: AsyncSession,
        questions: list[Question]
) -> int:
    insert_stmt = insert(QuestionModel).values(
        [question.dict() for question in questions]
    )
    insert_stmt = insert_stmt.on_conflict_do_nothing(
        index_elements=["id"],
    )
    res = await session.execute(insert_stmt)
    await session.commit()
    return res.rowcount


async def get_last_question(session: AsyncSession):
    stmt = (
        select(QuestionModel).order_by(QuestionModel.local_created_at.desc()).limit(1)
    )
    res = await session.execute(stmt)
    return res.scalar()
