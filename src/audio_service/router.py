from fastapi import APIRouter, Depends, File, HTTPException, status
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.audio_service.models import Record
from src.audio_service.schemas import UserCreateIn, UserCreateOut
from src.audio_service.service import create_user_in_db
from src.dependencies import get_session

router = APIRouter(
    prefix="/record",
    tags=["Records"],
)


@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    description="Create users",
    response_model=UserCreateOut,
)
async def create_user(
    user_create: UserCreateIn,
    session: AsyncSession = Depends(get_session)
):
    try:
        user = await create_user_in_db(user_create.username, session)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )



# @router.post("/")
# async def create_record(
#     user_id: str,
#     access_token: str,
#     wav_file: bytes = File(),
#     session: AsyncSession = Depends(get_session),
# ):
#     stmt = insert(Record).values(
#         user_id=user_id,
#         data=wav_file,
#         access_token=access_token,
#     )
#     await session.execute(stmt)
#     await session.commit()
