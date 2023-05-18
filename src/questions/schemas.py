from datetime import datetime

from pydantic import BaseModel, validator


class Question(BaseModel):
    id: int
    answer: str
    question: str
    created_at: datetime

    @validator("created_at")
    def strip_timezone(cls, v: datetime):
        return v.replace(tzinfo=None)

    class Config:
        orm_mode = True


class QuestionsCreate(BaseModel):
    questions_num: int
