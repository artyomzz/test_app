from fastapi import APIRouter, Depends, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_client, get_session
from src.questions.schemas import Question, QuestionsCreate
from src.questions.service import (fetch_questions, get_last_question,
                                   save_questions_to_db)

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Fetch questions and save them to DB",
    response_model=Question | None,
)
async def create_questions(
    questions_create: QuestionsCreate,
    client: AsyncClient = Depends(get_client),
    session: AsyncSession = Depends(get_session),
) -> Question | None:
    num_questions = questions_create.questions_num
    questions = await fetch_questions(
        client=client,
        questions_num=num_questions,
    )
    num_inserted = await save_questions_to_db(session, questions)
    if num_inserted >= 0 and num_questions - num_inserted > 0:
        return await create_questions(
            QuestionsCreate(questions_num=num_questions - num_inserted),
            client,
            session,
        )

    return await get_last_question(session)
