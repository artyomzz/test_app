import asyncio
from uuid import UUID, uuid4

import aiofiles
import aiofiles.os
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from src.audio_service.schemas import RecordCreateOut, UserCreateIn, UserCreateOut
from src.audio_service.service import (
    convert_to_mp3,
    create_user_in_db,
    get_record_from_db,
    save_record_to_db,
)
from src.config import CHUNK_SIZE
from src.dependencies import get_session

router = APIRouter(
    prefix="/record",
    tags=["Records"],
)


@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint to create users",
    response_model=UserCreateOut,
)
async def create_user(
    user_create: UserCreateIn, session: AsyncSession = Depends(get_session)
):
    try:
        user = await create_user_in_db(user_create.username, session)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint to upload records",
    response_model=RecordCreateOut,
)
async def upload_record(
    user_id: UUID,
    access_token: UUID,
    wav_file: UploadFile,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    if wav_file.content_type != "audio/wav":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Wrong file format. Only wav is supported.",
        )
    wav_filename = wav_file.filename or f"{uuid4()}.wav"
    mp3_filename = f"{uuid4()}.mp3"
    try:
        async with aiofiles.open(wav_filename, "wb") as f:
            while chunk := await wav_file.read(CHUNK_SIZE):
                await f.write(chunk)
        # potentially long task
        await run_in_threadpool(convert_to_mp3, wav_filename, mp3_filename)

        # save file
        async with aiofiles.open(mp3_filename, "rb") as f:
            content = await f.read()
            record = await save_record_to_db(
                user_id=user_id,
                access_token=access_token,
                content=content,
                session=session,
            )
            return RecordCreateOut(
                url="http://{}:8000/record?id={}&user_id={}".format(
                    request.client.host, record.id, user_id
                )
            )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Erorr in saving record to db",
                "err": str(e),
            },
        )
    finally:
        await asyncio.gather(
            aiofiles.os.remove(wav_filename), aiofiles.os.remove(mp3_filename)
        )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Endpoint to download records",
    response_class=Response,
)
async def download_record(
    id: UUID, user_id: UUID, session: AsyncSession = Depends(get_session)
):
    record = await get_record_from_db(
        id=id,
        user_id=user_id,
        session=session,
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    content_disposition = f'attachment; filename="{uuid4()}.mp3"'

    return Response(
        content=record.data,
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": content_disposition,
        },
        status_code=status.HTTP_200_OK,
    )
